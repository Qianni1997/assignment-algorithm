---
Qianni Wang
2018/11/21 18:50
---

# MSA与FW算法在sf与cs网络上的应用

## 1. 使用方法：

1. 安装matplotlib库（若没有可将绘图部分与导入模块命令注释掉）
2. 将压缩包解压，打开**MSA_FW_pannel**文件，可修改“NETWORK”与“METHOD”参数，而后运行。
3. 可修改32行：RG_list = MSA_assignment(LINK, NODE, ORIGIN, LINK_COUNT,k0 = 2000, eps = pow(10,-4))的最大循环步数k0与收敛精度eps参数。同理可修改34行：FW算法相关参数。

4. MSA_FW_pannel文件运行后输出：

① 最终状态各link流量

② 运行时间

③ Relative Gap随循环变化情况

5. 其余内容（类、函数）写在**MSA_FW_obj**文件中。

## 2. 类的属性与方法

   ### 2.1 Node类

#### 属性

**node_id** 节点编号; **l_in** 流入节点的路段对象构成的列表; **l_out** 流出节点的路段对象构成的列表; 

**u** 最短路中该节点cost标号; **p** 最短路中该节点前序节点标号

#### 方法

**set_l_in** 向流入路段列表末尾添加一个路段对象; **set_l_out** 向流出路段列表末尾添加一个路段对象; **set_SPP_u** 设置cost标号; **set_SPP_p** 设置前序节点标号

### 2.2 Link类

#### 属性

**link_id** 路段编号, **tail_node** 路段起点（相当于from node）, **head_node** 路段终点（相当于to node), **capacity** 路段容量, **length** 路段长度, **free_flow_time** 路段自由流时间, **b** 路段BPR函数系数(alpha), **power**(beta) 路段BPR函数指数,**speed_limit** 路段限速, **toll** 路段收费, **link_type** 路段类型, **x_flow** 路段流量（x_a）, **cost** 路段cost（t_a）, **y_flow** 下降方向流量

#### 方法

**LPF** BPR函数设置路段cost; **set_x_flow** 设置路段流量; **empty_y_flow** 清零下降方向流量; **add_x_flow** x_flow在原有基础上叠加(用于第一次all-or-nothing)；**add_y_flow** 下降方向流量在原有基础上叠加

### 2.3 Destination类

#### 属性

**o_id** O的节点编号node_id, **d_id** D的节点编号node_id, **demand** OD对的需求, **splink** 由最短路路段对象组成的最短路列表

#### 方法

**set_SP** 在已有指定O点计算出的前序节点列表shortestpath_p_list的基础上得到splink最短路列表

### 2.4 Origin类

#### 属性

**o_id** Origin的节点编号node_id, **destination** 包含该O为起点的全部OD对destination对象构成的字典，字典键为D的节点编号，值为destination对象

#### 方法

**set_destination** 设置destination字典; **calc_SP** 计算以O为起点时，所有node的最短路的前序节点集

## 3.外部函数

#### 3.1 文件读取与对象创建

**read_net_create_LINK_NODE**, 读取net文件，建立LINK、NODE的list保存Link、Node类的实例

**read_trp_create_ORIGIN**, 读取trp文件，建立ORIGIN与destination_dict的dictionary保存Origin、Destination类的实例

#### 3.2 Relative Gap相对误差计算

**calc_SPcost**, 计算一个OD pair间最短路的cost

**calc_sum_SPcost_multiply_demand**, 计算路网中各个OD pair的最短路cost与OD pair需求乘积的和

**calc_sum_x_flow_multiply_cost**, 计算路网中各个link的流量x_flow与link cost乘积的和

**calc_relative_gap**, 计算相对误差：

$$ RG=\frac{\sum_{(r,s)} u_{(r,s)}d_{(r,s)}}{\sum_{(i,j)}x_{(i,j)}t(x_{(i,j)})}$$

#### 3.3 FW与MSA算法

**FW_line_search**, 找到$\alpha$使得目标函数在下降方向取得最小值

**MSA_assignment**, 运行MSA算法

**TEST_FW**, 运行FW算法