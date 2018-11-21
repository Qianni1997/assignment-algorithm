# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 20:08:53 2018

@author: Qianni Wang
"""
"""
类名：首字母大写 Node Link Origin Destination
承载类的对象的容器：全部字母大写 NODE LINK ORIGIN
其中NODE、LINK为list，0位置废掉，下标代表编号
ORIGIN为dictionary，下标代表编号
ORIGIN[i].destination为装载Destination对象的字典，ORIGIN[i].destination[j]代表以i为O，以j为D的Destination对象
"""

##################################
#设置网络名称
##################################

NETWORK = 'sf' # sf = SiousFall；cs = ChicagoSketch

##################################
#建立Node,Link,Origin,Destination类
##################################
"""
属性：
node_id 节点编号; l_in 流入节点的路段对象构成的列表; l_out 流出节点的路段对象构成的列表; 
u 最短路中该节点cost标号; p 最短路中该节点前序节点标号
方法：
set_l_in 向流入路段列表末尾添加一个路段对象; set_l_out 向流出路段列表末尾添加一个路段对象;
set_SPP_u 设置cost标号; set_SPP_p 设置前序节点标号
"""
class Node:
    def __init__(self, node_id, l_in_empty, l_out_empty):
        self.node_id = node_id
        self.l_in = l_in_empty
        self.l_out = l_out_empty
    def set_l_in(self, l_in):
        self.l_in.append(l_in)
    def set_l_out(self, l_out ):
        self.l_out.append(l_out)
    def set_SPP_u(self, u):
        self.u = u
    def set_SPP_p(self,p):
        self.p = p
"""
属性：
link_id 路段编号, tail_node 路段起点（相当于from node）, head_node 路段终点（相当于to node), 
capacity 路段容量, length 路段长度, free_flow_time 路段自由流时间, b 路段BPR函数系数(alpha), power(beta) 路段BPR函数指数,
speed_limit 路段限速, toll 路段收费, link_type 路段类型, x_flow 路段流量（x_a）, cost 路段cost（t_a）, y_flow 下降方向流量
方法：
LPF BPR函数设置路段cost; set_x_flow 设置路段流量; empty_y_flow 清零下降方向流量; add_y_flow 下降方向流量在原有基础上叠加
"""
class Link:
    def __init__(self, link_id, tail_node, head_node, capacity, \
                 length, free_flow_time, b, power, speed_limit, \
                 toll, link_type, x_flow):
        self.link_id = link_id
        self.tail_node = tail_node
        self.head_node = head_node
        self.capacity = capacity
        self.length = length
        self.free_flow_time = free_flow_time
        self.b = b
        self.power = power
        self.speed_limit = speed_limit
        self.toll = toll
        self.link_type = link_type
        self.x_flow = x_flow
    def LPF(self, x_flow, free_flow_time, capacity, b, power):
        cost = free_flow_time*(1+b*pow((x_flow/capacity),power))
        self.cost = cost
        return self.cost
    def set_x_flow(self, x_flow):
        self.x_flow = x_flow
    def empty_y_flow(self):
        self.y_flow = 0
    def add_y_flow(self, add_flow):
        try:
            self.y_flow += add_flow
        except:
            self.y_flow =0
            self.y_flow += add_flow
"""
Destination的对象实际为OD对
属性：
o_id O的节点编号node_id, d_id D的节点编号node_id, demand OD对的需求, splink 由最短路路段对象组成的最短路列表
方法：
set_SP 在已有指定O点计算出的前序节点列表shortestpath_p_list的基础上得到splink最短路列表
"""        
class Destination:
    def __init__(self, d_id, o_id, demand):
        self.d_id = d_id
        self.o_id = o_id
        self.demand = demand
    def set_SP(self,o_id, d_id, shortestpath_p_list,node):
        if shortestpath_p_list[o_id] == -1:
            pass
        else:
            print('shortestpath_p_list is wrong!')
        shortestpath_link=[]
        head_n = node[d_id]
        tail_n = shortestpath_p_list[d_id]
        while tail_n != -1:
            for l in head_n.l_in:
                if l.tail_node == tail_n.node_id:
                    shortestpath_link.insert(0,l)
            head_n = tail_n
            tail_n = shortestpath_p_list[head_n.node_id]
        self.splink = shortestpath_link
            
"""
Origin对象包括该点为起点的所有Destination对象
属性：
o_id Origin的节点编号node_id, destination 包含该O为起点的全部OD对destination对象构成的字典，字典键为D的节点编号，值为destination对象
方法：
set_destination 设置destination字典; calc_SP 计算以O为起点时，所有node的最短路的前序节点集
"""   
class Origin:
    def __init__(self, o_id):  
        self.o_id = o_id  
    def set_destination(self,destination):
        self.destination = destination
    def calc_SP(self, o_id, node):
        #initialize
        node[o_id].set_SPP_u(0)
        for t in node[1:]:
            t.set_SPP_p(-1)
            if t.node_id != o_id:
                t.set_SPP_u(float('inf'))
        #mainloop
        Q = [node[o_id]]
        while len(Q) != 0:
            i = Q[0]
            del Q[0]
            for ij in i.l_out:
                j = node[ij.head_node]
                if j.u > (i.u+ij.cost):
                    j.u = (i.u+ij.cost)
                    j.p = i#id还是对象
                    if j not in Q:
                        Q.append(j)
        shortestpath_p_list = [0]
        for t in node[1:]:
            shortestpath_p_list.append(t.p)
        return shortestpath_p_list
##################################
#读取网络文件
##################################
with open('%s_net.txt'%NETWORK, 'r') as f1:
    l1 = f1.readlines()
#去除空行
length=len(l1)
x=0
while x < length:
    if l1[x] == '\n':
        del l1[x]
        x -= 1
        length -= 1
    x += 1
for i in range(len(l1)):
    if '~' in l1[i]:
        l1_START_LINE = i+1
        break
# str modify
for i in range(5):
    l1[i] = l1[i].split(' ')
NODE_COUNT = eval(l1[1][-1])
LINK_COUNT = eval(l1[3][-1])
for i in range(l1_START_LINE, len(l1)):
    l1[i] = l1[i].rstrip('\n')
    l1[i] = l1[i].rstrip(';')
    l1[i] = l1[i].rstrip('\t')
    l1[i] = l1[i].lstrip('\t')
    l1[i] = l1[i].split('\t')
readlist = l1[l1_START_LINE:]
##################################
#建立 Link与Node对象，并放入LINK、NODE容器
##################################
LINK = [Link(i+1,eval(readlist[i][0]),eval(readlist[i][1]),\
                  eval(readlist[i][2]),eval(readlist[i][3]),\
                  eval(readlist[i][4]),eval(readlist[i][5]),\
                  eval(readlist[i][6]),eval(readlist[i][7]),\
                  eval(readlist[i][8]),eval(readlist[i][9]),0) for i in range(LINK_COUNT)]
LINK.insert(0, 0)#in order to avoid different meanings between index and id
# create node object and put them into NODE_LIST
NODE = [Node(i+1,[],[]) for i in range(NODE_COUNT)]
NODE.insert(0, 0)
# rectify l_in and l_out
for i in range (1, LINK_COUNT+1):
    NODE[LINK[i].tail_node].set_l_out(LINK[i])
    NODE[LINK[i].head_node].set_l_in(LINK[i])
##################################
#读取 trip demand文件
##################################
with open('%s_trp.txt'%NETWORK, 'r') as f2:
    l2 = f2.readlines()
length=len(l2)
x=0
while x < length:
    if l2[x] == '\n':
        # l.remove(l[x])
        del l2[x]
        x -= 1
        length -= 1
    x += 1

# str modify
for i in range(3):
    l2[i] = l2[i].split(' ')
FLOW_COUNT = eval(l2[1][-1])

changelinecount = 0
changeline=[]
for i in range(len(l2)):
    if 'Origin' in l2[i]:
        changeline.append(i)
        changelinecount += 1
l2_START_LINE = changeline[0]

changelinerolling = changeline[1:]
changelinerolling.append(len(l2))      
for i,t in zip(changeline,changelinerolling):
    l2[i] = l2[i].rstrip('\n')
    if NETWORK == 'sf':  
        l2[i] = l2[i].replace(' ','')
        l2[i] = l2[i].split('\t')
    elif NETWORK == 'cs':
        l2[i] = l2[i].split(' ')
    for j in range(1,t-i):
        l2[i+j] = l2[i+j].rstrip('\n')
        l2[i+j] = l2[i+j].replace(' ','')
        l2[i+j] = l2[i+j].rstrip(';')
        l2[i+j] = l2[i+j].split(';')
#flatten demand
readlist2=[]
for i,t in zip(changeline, changelinerolling):
    readlist2.append([l2[i][0],l2[i][-1]])
    ext = []
    for j in range(1,t-i):
        ext.extend(l2[i+j])
    readlist2.append(ext)
    
##################################
#建立 Origin与Destination对象，并放入destination_dict与ORIGIN容器
##################################
ORIGIN={}
for i in range(0,len(readlist2),2):
    destination_dict = {}
    o_id = eval(readlist2[i][-1])
    ORIGIN[o_id] = Origin(o_id)
    for j in range(len(readlist2[i+1])):
        d_id, demand = eval(readlist2[i+1][j].split(':')[0]),eval(readlist2[i+1][j].split(':')[-1])
        destination_dict[d_id] = Destination(o_id, d_id ,demand)
    ORIGIN[o_id].set_destination(destination_dict)

##################################
#MSA分配
##################################
#initialize
k = 0
for ii in LINK[1:]:
    ii.LPF(0, ii.free_flow_time, ii.capacity, ii.b, ii.power)
eps0 = pow(10,-6) 
K0 = 10000
g = float('inf')
#main loop
while (k<K0) & (g>eps0):
    g_sum = 0
    alpha = 1/(1+k)
    #find shorest path of the whole newtork
    for o_id,o_obj in zip(ORIGIN.keys(),ORIGIN.values()):
        shortestpath_p_list = o_obj.calc_SP(o_id, NODE)
        for d_id,d_obj in zip(o_obj.destination.keys(),o_obj.destination.values()):
            d_obj.set_SP(o_id, d_id, shortestpath_p_list, NODE)
    #all or nothing assignment
    for aa in range(1,LINK_COUNT+1):
        LINK[aa].empty_y_flow()
    for o_id in ORIGIN.keys(): 
        for d_id in ORIGIN[o_id].destination.keys():
            spln = len(ORIGIN[o_id].destination[d_id].splink)
            q_flow = ORIGIN[o_id].destination[d_id].demand
            for ll in range(spln):
                ORIGIN[o_id].destination[d_id].splink[ll].add_y_flow(q_flow)
    for aa in range(1,LINK_COUNT+1):
        g_sum -= (LINK[aa].cost*(LINK[aa].y_flow-LINK[aa].x_flow))
        LINK[aa].set_x_flow(LINK[aa].x_flow + alpha*(LINK[aa].y_flow-LINK[aa].x_flow))
        LINK[aa].LPF(LINK[aa].x_flow, LINK[aa].free_flow_time, LINK[aa].capacity, LINK[aa].b, LINK[aa].power)
    k += 1
    g = abs(g_sum)
##################################
#输入均衡后各路段流量结果
##################################
for aa in range(1,LINK_COUNT+1):
    print(aa,':',LINK[aa].x_flow)

