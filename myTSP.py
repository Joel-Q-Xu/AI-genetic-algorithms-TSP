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
plt.ion()
import matplotlib
#显示中文
matplotlib.rcParams['font.family']= 'SimHei'
import math
import random
import tkinter
import time
start = time.perf_counter()

#获得总距离
def get_sum_distance(group,origin):
	distance=0
	distance+=state[origin][group[0]]
	for i in range(len(group)):
		if i == len(group)-1:
			distance+=state[origin][group[i]]
		else:
			distance+=state[group[i]][group[i+1]]
	return distance
			
	

#自然选择
""" 对适应度从大到小排序，选出存活的染色体
    再进行随机选择，选出适应度虽然小，但是幸存下来的个体
"""	
def select(population,origin):
	#对总距离从小到大进行排序
	dis=[[get_sum_distance(group,origin),group] for group in population]
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
    child_count=count-len(parents)
    #孩子列表
    child=[]
    while len(child)<child_count:
        index1=random.randint(0,len(parents)-1)
        index2=random.randint(0,len(parents)-1)
        if index1!=index2:
            dex1=parents[index1]
            dex2=parents[index2]
            if random.random()<px:

                left=random.randint(0,len(dex1)-2)
                right_1=random.randint(left+1,len(dex1)-1)
                #由于列表索引特性，将right设为交叉片段后第一个基因索引
                right=right_1+1

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
            else:
                child.append(dex1)
                child.append(dex2)
    return child

#变异
"""
按照给定的变异率，对选定变异的个体，随机地取三个整数，满足 1<u<v<w<33 ，把 v 、u之间（包括u 和v）的基因段插到w后面。 
"""
def change(child):
    for i in range(len(child)):
        if random.random()<pm:
            change_child=child[i]
            u=random.randint(1,len(change_child)-2)
            v=random.randint(u+1,len(change_child)-1)
            w=random.randint(v+1,len(change_child))
            change_child=change_child[0:u]+change_child[v+1:w+1]+change_child[u:v+1]+change_child[w+1:]
            child[i]=change_child
    return child

def get_best(population,origin):
	dis=[[get_sum_distance(group,origin),group] for group in population]
	dis=sorted(dis)
	return dis[0][0],dis[0][1]

#主函数
def TSP():
    city_index=[]
    choose_city=text1.get()
    pass_city=text2.get().split(",")

    origin=city_name.index(choose_city)
    for item in pass_city:
        cityNo=city_name.index(item)
        city_index.append(cityNo)
    

    population=[]			#初始化种群
    for i in range(count):
        group=city_index.copy()
        random.shuffle(group)   #将序列的所有元素随机排序
        population.append(group)

    #存放过程中的距离，验证算法找出最优解
    res=[]
    distance,path=get_best(population,origin)
    for i in range(evolution_time):
        parents=select(population,origin) 	#选择
        child=exchange(parents)    	#交叉
        child=change(child)		#变异
        population=parents+child	#更新种群
        distance,path=get_best(population,origin)
        res.append(distance)

    result_path=[origin]+path+[origin]
    print("distance: ",distance)
    print("passby: ",result_path)

    color=["b","g","r","y","c","k","m"]
    for item in range(city_num):
        if city_name[item]==choose_city:
            plt.plot(city_state[item,0],city_state[item,1],"*",color='r',markersize=20)
        else:
            plt.plot(city_state[item,0],city_state[item,1],"o",color='b')
        plt.text(city_state[item,0]+0.1,city_state[item,1]+0.1,city_name[item])



    for item in range(1,len(result_path)):
        x=[]
        y=[]
        x.append(city_state[result_path[item-1],0])
        y.append(city_state[result_path[item-1],1])
        x.append(city_state[result_path[item],0]) #两点中心
        y.append(city_state[result_path[item],1])
        center_x,center_y=(x[0]+x[1])/2,(y[0]+y[1])/2
        plt.plot(x,y,"-",color=color[item%len(color)]) 
        plt.text(center_x+1,center_y+1,item,fontsize="large",color='g')

    #plt.show()    
    end = time.perf_counter()
    print('Running time: %s Seconds'%(end-start))
    label4['text'] = 'Running time:' +str(end-start) +'Seconds'

    #plt.figure()
    #plt.plot(list(range(len(res))),res)
    #plt.show()



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
count=100 		#种群规模
init_count =1000 	#改进次数 
evolution_time=3000  	#进化次数 
pm=0.8  		#变异率   
ps=0.3			#强者比例 
pr=0.5			#弱者存活率
px=0.4                 #交叉概率
    
root=tkinter.Tk() #生成root主窗口
root.title('Welcome To TSP Map')  
root.geometry('360x270')
label1=tkinter.Label(root,text='可选择的城市有：\n北京,天津,上海,重庆,拉萨,乌鲁木齐,银川,呼和浩特,南宁,哈尔滨,\n长春,沈阳,石家庄,太原,西宁,济南,郑州,南京,合肥,杭州,福州,南昌,\n长沙,武汉,广州,台北,海口,兰州,西安,成都,贵阳,昆明,香港,澳门') #生成标签
label1.pack()        #将标签添加到主窗口

label2=tkinter.Label(root,text='input your starting city:')
label2.pack()  

text1 = tkinter.StringVar()  
text1.set('')  
entry = tkinter.Entry(root,width=200) 
entry['textvariable'] = text1  
entry.pack() 

label3=tkinter.Label(root,text='input your passing city:')
label3.pack()  

text2 = tkinter.StringVar()  
text2.set('')  
entry = tkinter.Entry(root,width=200) 
entry['textvariable'] = text2 
entry.pack() 

button=tkinter.Button(root,text='Starting Calculation',command=TSP) #生成button1
button.pack()         #将button1添加到root主窗口
label4=tkinter.Label(root,text='Running time')
label4.pack()
root.mainloop()    

