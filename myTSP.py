#-*-coding:utf-8 -*-
"""
参数设计：种群规模count=100，染色体长度length=33，进化次数evolution_time=5000
编码策略:采用十进制.直接用城市的编号进行编码，染色体{1，2，……33}表示路径为15-1-2-……-33。
"""
"""
参数说明：
origin #起点0-33->对应城市
state[][] -----城市坐标
init_count ----改进次数 1000
evolution_time 进化次数 5000
count  --------种群规模 100
pm  -----------变异率   0.1
ps  -----------强者比例 0.3
pr ------------弱者存活率 0.5
population[]---初始化种群
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import math
import random


#获得总距离
def get_sum_distance(group):
	distance=0
	distance+=state[origin][group[0]]
	for i in range(len(group)):
		if i == len(group)-1:
			distance+=state[origin][group[i]]
		else:
			distance+=state[group[i]][group[i+1]]
	return distance
			
	
#初始化种群
"""随机生成一个染色体，任意交换两个城市之间经过顺序，若总距离间歇性，则改变染色体，重复直至最佳"""
def init_group(group):
	i=0
	distance=get_sum_distance(group)
	while i<init_count:
		m=random.randint(0,len(group))
		n=random.randint(0,len(group))
		if m!=n:
			new_group=group.copy()
			t=new_group[m]
			new_group[m]=new_group[n]
			new_group[n]=t
			new_distance=get_sum_distance(new_group)
			if new_distance<distance:
				distance=new_distance
				group=new_group.copy()
		else:
			continue
		i+=1
		
#自然选择
""" 对适应度从大到小排序，选出存活的染色体
    再进行随机选择，选出适应度虽然小，但是幸存下来的个体
"""	
def select(population):
	#对总距离从小到大进行排序
	dis=[[get_sum_distance(group),group] for group in population]
	dis=[group[1] for group in sorted(dis)]
	#选出存活的染色体
	survive=int(len(dis)*ps)
	parents=dis[:survive]
	#选出适应度虽然小，但是幸存下来的个体
	for choose in dis[survive:]:
		if random.random()<pr:
			parents.append(choose)
	return parents

#交叉
"""随机在双亲中选择两个交叉点，再交换片段 ，采用次序杂交法--------防止交叉后染色体重复"""
def exchange(parents):
	#生成子代的个数,以此保证种群稳定
    target_count=count-len(parents)
    #孩子列表
    child=[]
    while len(child)<target_count:
        index1=random.randint(0,len(parents)-1)
        index2=random.randint(0,len(parents)-1)
        if index1!=index2:
            dex1=parents[index1]
            dex2=parents[index2]

            left=random.randint(0,len(dex1)-2)
            right=random.randint(left+1,len(dex1)-1)

            gene1=dex1[left:right]
            gene2=dex2[left:right]
            
            child_1=dex1[right:]+dex1[:right]
            child_2=dex2[right:]+dex2[:right]
            child1=child_1.copy()
            child2=child_2.copy()

            for g in gene1:
                child_2.remove(g)
            for g in gene2:
                child_1.remove(g)

            child1[left:right]=gene2
            child2[left:right]=gene1
            child1[right:]=child_1[0:len(child1)-right]
            child1[:left]=child_1[len(child1)-right:]
    
            child2[right:]=child_2[0:len(child2)-right]
            child2[:left]=child_2[len(child2)-right:]
            child.append(child1)
            child.append(child2)
    return child

#变异
"""
按照给定的变异率，对选定变异的个体，随机地取三个整数，满足 1<u<v<w<33 ，把 v 、u之间（包括u 和v）的基因段插到w后面。 
"""
def change(child):
	for i in range(len(child)):
		if random.random()<pm:
			u=random.randint(1,len(child)-4)
			v=random.randint(u+1,len(child)-3)
			w=random.randint(v+1,len(child)-2)
			change_child=child[i]
			change_child=change_child[0:u]+change_child[v:w]+change_child[u:v]+change_child[w:]

def get_best(population):
	dis=[[get_sum_distance(group),group] for group in population]
	dis=sorted(dis)
	return dis[0][0],dis[0][1]

#主函数
city_name=[]
city_state=[]
with open("data.txt","r")as f:
    lines=f.readlines()
    for line in lines:
        line=line.strip().split(",")
        city_name.append(line[0])
        city_state.append([float(line[1]),float(line[2])])
city_state=np.array(city_state)

#距离矩阵
city_num=len(city_name)
state=np.zeros([city_num,city_num])
for i in range(city_num):
	for j in range(city_num):
		state[i][j]=math.sqrt((city_state[i][0]-city_state[j][0])**2+(city_state[i][1]-city_state[j][1])**2)

#参数设置
count=100 				#种群规模
init_count =1000 		#改进次数 
evolution_time=5000  	#进化次数 
pm=0.1  				#变异率   
ps=0.3					#强者比例 0.3
pr=0.5					#弱者存活率 
choose_city=input("input your starting point:")  #选择起点
origin=city_name.index(choose_city)
city_index=[i for i in range(city_num)]
city_index.remove(origin)
population=[]			#初始化种群
for i in range(1,count):
	group=city_index.copy()
	random.shuffle(group)   #将序列的所有元素随机排序
	#init_group(group)
	population.append(group)

#存放过程中的距离，验证算法找出最优解
res=[]
distance,path=get_best(population)
for i in range(1,evolution_time):
	parents=select(population) 	#选择
	child=exchange(parents)    	#交叉
	change(child)				#变异
	population=parents+child	#更新种群
	distance,path=get_best(population)
	res.append(distance)

result_path=[origin]+path+[origin]
print(distance)
print(result_path)


x=[]
y=[]
for item in result_path:
	x.append(city_state[item,0])
	y.append(city_state[item,1])

plt.plot(x,y,"-o")
plt.show()

plt.plot(list(range(len(res))),res)
plt.show()

