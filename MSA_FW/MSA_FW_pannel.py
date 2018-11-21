# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 10:35:20 2018

@author: lenovo
"""
"""
类名：首字母大写 Node Link Origin Destination
承载类的对象的容器：全部字母大写 NODE LINK ORIGIN
其中NODE、LINK为list，0位置废掉，下标代表编号
ORIGIN为dictionary，下标代表编号
ORIGIN[i].destination为装载Destination对象的字典，ORIGIN[i].destination[j]代表以i为O，以j为D的Destination对象
"""
import time
import matplotlib.pyplot as plt
from MSAobj import Node, Link,\
 Destination, Origin,read_net_create_LINK_NODE, \
 read_trp_create_ORIGIN, calc_SPcost, calc_sum_SPcost_multiply_demand, \
 calc_sum_x_flow_multiply_cost, calc_relative_gap, MSA_assignment, FW_line_search, TEST_FW
##################################
#设置网络名称，计算算法
##################################
start = time.clock()
NETWORK = 'sf'# sf = SiousFall;cs = ChicagoSketch
METHOD = 'FW' #FW = Frank-Wolfe; MSA
##################################
#调用函数
##################################
LINK, NODE, NODE_COUNT, LINK_COUNT = read_net_create_LINK_NODE(NETWORK)
ORIGIN,FLOW_COUNT = read_trp_create_ORIGIN(NETWORK)
if METHOD=='MSA':
    RG_list = MSA_assignment(LINK, NODE, ORIGIN, LINK_COUNT,k0 = 2000, eps = pow(10,-4))
elif METHOD=='FW':   
    RG_list = TEST_FW(LINK, NODE, ORIGIN, LINK_COUNT, k0= 2000, k1=10, eps = pow(10,-4) , eps1= pow(10,-3) , eps2=pow(10,-2))
else:
    pass
end = time.clock()
##################################
#输入均衡后各路段流量结果
##################################
for aa in range(1,LINK_COUNT+1):
    print(aa,':',LINK[aa].x_flow)
#绘制relative gap 曲线图
def plot_RG(data_list, network, method):
    if method == 'FW':
        plt.plot(data_list,'o-',c='r')
    elif method =='MSA':
        plt.plot(data_list,'o-',c='b')
    else:
        plt.plot(data_list,'o-',c='g')
    if network == 'sf':
        plt.title('Sious Fall using %s algorithm'%method)
    elif network == 'cs':
        plt.title('Chicago Sketch using %s algorithm' %method)
    else:
        pass
    plt.xlabel('STEP')
    plt.ylabel('RG')
plot_RG(RG_list, NETWORK, METHOD)
print('total time=',end-start,'s')