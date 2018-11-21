# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 20:08:53 2018

@author: Qianni Wang
"""
NETWORK = 'sf' 
# sf = SiousFall
# cs = ChicagoSketch

#类名：首字母大写 Node Link Origin Destination
#承载类的对象的容器：全部字母大写 NODE LINK ORIGIN
#其中NODE、LINK为list，0位置废掉，下标代表编号
#ORIGIN为dictionary，下标同样代表编号
#########################################################################################
#########################################################################################
# create class
class Node:
    def __init__(self, node_id, l_in_empty, l_out_empty):
        self.node_id = node_id
        self.l_in = l_in_empty
        self.l_out = l_out_empty

    def set_l_in(self, l_in):
        self.l_in.append(l_in)
    def set_l_out(self, l_out ):
        self.l_out.append(l_out)

class Link:
    def __init__(self, link_id, tail_node, head_node, capacity, length, free_flow_time, beta, power, speed_limit, toll, link_type):
        self.link_id = link_id
        self.tail_node = tail_node
        self.head_node = head_node
        self.capacity = capacity
        self.length = length
        self.free_flow_time = free_flow_time
        self.beta = beta
        self.power = power
        self.speed_limit = speed_limit
        self.toll = toll
        self.link_type = link_type
        
class Destination:
    def __init__(self, d_id, o_id, demand):
        self.d_id = d_id
        self.o_id = o_id
        self.demand = demand

class Origin:
    def __init__(self, o_id):  
        self.o_id = o_id  
        #self.destination = destination_empty
    def set_destination(self,destination):
        #self.destination.append(destination)
        self.destination = destination
#########################################################################################
#########################################################################################
# open network file and read file
with open('%s_net.txt'%NETWORK, 'r') as f1:
    l1 = f1.readlines()
length=len(l1)
x=0
while x < length:
    if l1[x] == '\n':
        # l.remove(l[x])
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
# create link object and put them into LINK_LIST
LINK = [Link(i+1,eval(readlist[i][0]),eval(readlist[i][1]),\
                  eval(readlist[i][2]),eval(readlist[i][3]),\
                  eval(readlist[i][4]),eval(readlist[i][5]),\
                  eval(readlist[i][6]),eval(readlist[i][7]),\
                  eval(readlist[i][8]),eval(readlist[i][9])) for i in range(LINK_COUNT)]
LINK.insert(0, 0)#in order to avoid different meanings between index and id
# create node object and put them into NODE_LIST
NODE = [Node(i+1,[],[]) for i in range(NODE_COUNT)]
NODE.insert(0, 0)
# rectify l_in and l_out
for i in range (1, LINK_COUNT+1):
    NODE[LINK[i].tail_node].set_l_out(LINK[i])
    NODE[LINK[i].head_node].set_l_in(LINK[i])
#########################################################################################
#########################################################################################      
# open flow file and read file
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
    
#########################################################################################
#########################################################################################
#create origin and destination objects
ORIGIN={}
for i in range(0,len(readlist2),2):
    destination_dict = {}
    o_id = eval(readlist2[i][-1])
    ORIGIN[o_id] = Origin(o_id)
    for j in range(len(readlist2[i+1])):
        d_id, demand = eval(readlist2[i+1][j].split(':')[0]),eval(readlist2[i+1][j].split(':')[-1])
        destination_dict[d_id] = Destination(o_id, d_id ,demand)
    ORIGIN[o_id].set_destination(destination_dict)






