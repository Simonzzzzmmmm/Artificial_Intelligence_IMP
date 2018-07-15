# coding:utf-8
import random
import time
import matplotlib.pyplot as plt
def addtwodimdict(thedict, key_a, key_b, val):
    if key_a in thedict:
        thedict[key_a].update({key_b: val})
    else:
        thedict.update({key_a:{key_b: val}})

def get_graph(filename):
    f = open(filename,'r')
    count = 0
    vertices = 0
    edge = 0
    list = []
    direct_dict = dict()
    new_char = []
    in_degree = {}
    out_degree = {}
    for r in f.readlines():
        list.append(r.split(" "))
        if count == 0:
            vertices = list[0][0]
            edge = list[0][1]
            for j in range(int(vertices)+1):
                in_degree[j] = 0
                out_degree[j] = 0
        if count != 0:
            new_char.append(list[count][2].split('\n'))
            addtwodimdict(direct_dict,int(list[count][0]),int(list[count][1]),float(new_char[count-1][0]))
            in_degree[int(list[count][1])] = round(1/float(new_char[count-1][0]))
            out_degree[int(list[count][0])] = out_degree[int(list[count][0])]+1
        count = count + 1
    in_table = {}
    for i in direct_dict.keys():
        for j in direct_dict[i].keys():
            addtwodimdict(in_table, j, i, i)
    return in_table,int(vertices),in_degree,out_degree,direct_dict
def create_random_list(vertices):
    random_list = {}
    for i in range(vertices):
        a = random.random()
        random_list[i+1] = a
    return random_list
#寻找种子结点的方法
def greedy_find(k,out_degree):
    max_value_nodes = []
    #new_out_degree为一个tuple
    new_out_degree = sorted(out_degree.iteritems(),key=lambda asd:asd[1],reverse=True)
    for i in range(k):
        max_value_nodes.append(new_out_degree[i][0])
    return max_value_nodes
'''-----------------------------------LT_model------------------------------------'''
def LT_model(seeds,vertices,in_degree,out_degree,graph,in_table):
    if len(seeds) == 0:
        return 0
    else:
        q = []
        ActivitySet = []
        # 创建一个激活列表，若激活，则置为True
        act_or_not = {}
        for i in range(vertices + 1):
            act_or_not[i] = False
        random_list = create_random_list(vertices+ 1)
        for i in random_list.keys():
            if random_list[i] == 0:
                q.append(i)
                ActivitySet.append(i)
        # seeds = greedy_find(k,out_degree)
        # 将种子结点加入队列
        for i in seeds:
            ActivitySet.append(i)
            q.append(i)
            act_or_not[i] = True
        count = len(ActivitySet)
        while len(ActivitySet)!=0:
            total_weight = 0
            newActicitySet = []
            for i in ActivitySet:
                if out_degree[i] > 0:
                    # 加入j个邻居到栈中
                    for j in graph[i].keys():
                        # 判断是否可以激活,对每一个领点进行判断
                        if act_or_not[j] == False:
                            for k in in_table[j].keys():
                                if act_or_not[k]==True:
                                    total_weight+=graph[k][j]
                            if total_weight >= random_list[j]:
                                newActicitySet.append(j)
                                act_or_not[j] = True
                            total_weight = 0
            count = count+len(newActicitySet)
            ActivitySet = newActicitySet
        return count
'''---------------------------------LT_model------------------------------------'''
'''---------------------------------IC model--------------------------------'''
def IC_model(seeds,vertices,in_degree,out_degree,graph,in_table):
    node_be_influenced = []
    act_or_not = {}
    for i in range(vertices):
        act_or_not[i+1] = False
    q = []
    for i in seeds:
        q.append(i)
        node_be_influenced.append(i)
        act_or_not[i] = True
    while len(q)!=0:
        i = q.pop()
        act_or_not[i] = True
        if out_degree[i]!=0:
            for j in graph[i].keys():
                a = random.uniform(0,1)
                if graph[i][j]>a and act_or_not[j] == False:
                    node_be_influenced.append(j)
                    q.append(j)
                    act_or_not[i] = True
    output = float(len(node_be_influenced))
    return output
'''---------------------------------筛选种子结点---------------------------------'''
def DIffusion_Degree(filename,iteration):
    in_table,vertices, in_degree, out_degree, graph = get_graph(filename)
    S = {}
    optimized_seeds = []
    for i in range(vertices):
        if out_degree[i+1]==0:
            Cdd = 0
            S[i+1] = Cdd
        #计算节点综合影响力
    for i in graph.keys():
        #个人影响力
        Cdd = 0.0
        for j in graph[i].keys():
            Cdd = Cdd+out_degree[i]*graph[i][j]
        #算周围节点的影响力
        Cd = 0.0
        for j in graph[i].keys():
            #如果该节点的相邻结点有出度
            if out_degree[j] !=0:
                for k in graph[j].keys():
                    Cd = Cd+out_degree[j]*graph[j][k]
        S[i] = Cd+Cdd
    new_s = sorted(S.iteritems(), key=lambda asd: asd[1], reverse=True)
    #取前k个当做种子结点
    for i in range(iteration):
       optimized_seeds.append(new_s[i][0])
    return optimized_seeds
def greedyfind(filename,out_degree,graph,number_choose):
    #取前十个作为候选结点
    seeds = DIffusion_Degree(filename,len(graph)/2)
    temp = {}
    for i in seeds:
        temp[i] = out_degree[i]
    new_temp = sorted(temp.iteritems(), key=lambda asd: asd[1], reverse=True)
    new_o_seeds = []
    for i in range(number_choose):
        new_o_seeds.append(new_temp[i][0])
    print seeds
    return new_o_seeds
'''---------------------------------筛选种子结点---------------------------------'''
'''---------------------------------迭代器-------------------------------------'''
def iteration(model,vertices,in_degree,out_degree,graph,seeds,N,in_table):
    sum = 0.0
    N = 10000
    for i in range(N):
        output = model(seeds, vertices, in_degree, out_degree, graph,in_table)
        sum = sum + output
    return sum/N
'''---------------------------------IC mocel----------------------------------'''
def main_run(filename,model,seeds):
    in_table,vertices,in_degree,out_degree,graph = get_graph(filename)
    # temp = [56, 58, 53, 48]#这个解更好
    N = 10000
    sum = iteration(model,vertices,in_degree,out_degree,graph,seeds,N,in_table)
    print sum
    return sum
def search_act_parent(graph,node,activate_list):
    number = 0
    weight = 0
    for i in graph.keys():
        for j in graph[i].keys():
            if j==node:
                weight = graph[i][j]
                if activate_list[i]==True:
                    number = number+1
    return  weight,number

def get_total_activated_weight(in_degree,activate_or_not,dict,node):
    #说明此点出度为0,则权重为0
    if in_degree[node]==0:
        return 0
    weight,count = search_act_parent(dict,node,activate_or_not)
    total_weight = weight*count
    return total_weight
def generate_seed(filename):
    f = open(filename,'r')
    list = []
    for r in f.readlines():
        r.split('\n')
        list.append(int(r))
    return  list

if __name__ == "__main__":
    filename = 'network.txt'
    temp1 = [56,58,53,48]#IC
    sum = main_run(filename,LT_model,temp1)

    #sum = main_run(IC_model, temp, filename)
