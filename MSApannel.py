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

from MSAobj import Node, Link, Destination, Origin,read_net_create_LINK_NODE, read_trp_create_ORIGIN, MSA_assignment, FW_line_search, TEST_FW
##################################
#设置网络名称
##################################
NETWORK = 'sf'# sf = SiousFall；cs = ChicagoSketch

##################################
#调用函数
##################################
LINK, NODE, NODE_COUNT, LINK_COUNT = read_net_create_LINK_NODE(NETWORK)
ORIGIN,FLOW_COUNT = read_trp_create_ORIGIN(NETWORK)
#MSA_assignment(LINK, NODE, ORIGIN, LINK_COUNT,k0= 1000, eps = pow(10,-3))
TEST_FW(LINK, NODE, ORIGIN, LINK_COUNT, k0= 200, k1=10, eps = 0.1 , eps1= pow(10,-3) , eps2=pow(10,-2))
##################################
#输入均衡后各路段流量结果
##################################
for aa in range(1,LINK_COUNT+1):
    print(aa,':',LINK[aa].x_flow)
