# coding:utf-8
# list = DIffusion_Degree(filename,10)
# print list
import time
# DIffusion_Degree(filename,1)
#计算得到每个点的入度出度
# seeds = DIffusion_Degree(filename,4,10)
# print seeds
# coding:utf-8
import random
import numpy as np
import Queue
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
    direct_dict = {}
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
            addtwodimdict(in_table,j,i,1)
    return in_table,int(vertices),in_degree,out_degree,direct_dict
def search_act_parent(graph,node,activate_list):
    number = 0
    weight = 0
    # for i in graph.keys():
    #     for j in graph[i].keys():
    #         if j==node:
    #             weight = graph[i][j]
    #             if activate_list[i]==True:
    #                 number = number+1
    for i in graph.keys():
        if activate_list[i]==True:
            for j in graph[i].keys():
                if j==node:
                    weight+=graph[i][j]
    return  weight

def create_random_list(vertices):
    random_list = {}
    for i in range(vertices):
        a = random.random()
        random_list[i+1] = a
    return random_list
def get_total_activated_weight(in_degree,activate_or_not,dict,node):
    #说明此点出度为0,则权重为0
    if in_degree[node]==0:
        return 0
    weight = search_act_parent(dict,node,activate_or_not)
    total_weight = weight
    return total_weight
def LT_model(seeds,vertices,in_degree,out_degree,graph,in_table):
    total_weight = 0
    if len(seeds) == 0:
        return 0
    else:
        node_be_influenced = []
        # 创建一个激活列表，若激活，则置为True
        act_or_not = {}
        for i in range(vertices + 1):
            act_or_not[i] = False
        random_list = create_random_list(vertices + 1)
        for i in random_list.keys():
            if random_list[i] == 0:
                node_be_influenced.append(i)
        # seeds = greedy_find(k,out_degree)

        # 将种子结点加入队列
        for i in seeds:
            node_be_influenced.append(i)
            act_or_not[i] = True
        count = len(node_be_influenced)
        while len(node_be_influenced) != 0:
            new_node = []
            for i in node_be_influenced:
                act_or_not[i] = True
                if out_degree[i] != 0:
                    # 加入j个邻居到栈中
                    for j in graph[i].keys():
                        # 判断是否可以激活,对每一个领点进行判断
                        if act_or_not[j] == False:
                            for k in in_table[j].keys():
                                if act_or_not[k] == True:
                                    total_weight += graph[k][j]
                            if total_weight >= random_list[j]:
                                new_node.append(j)
                                act_or_not[j] = True
                            total_weight = 0
            count = count + len(new_node)
            node_be_influenced = new_node
        return count
    # total_weight = 0
    # if len(seeds) == 0:
    #     return 0
    # else:
    #     q = []
    #     ActivitySet = []
    #     # 创建一个激活列表，若激活，则置为True
    #     act_or_not = {}
    #     for i in range(vertices + 1):
    #         act_or_not[i] = False
    #     random_list = create_random_list(vertices + 1)
    #     for i in random_list.keys():
    #         if random_list[i] == 0:
    #             q.append(i)
    #             ActivitySet.append(i)
    #     # seeds = greedy_find(k,out_degree)
    #
    #     # 将种子结点加入队列
    #     for i in seeds:
    #         ActivitySet.append(i)
    #         q.append(i)
    #         act_or_not[i] = True
    #     while len(q) != 0:
    #         i = q.pop()
    #         if out_degree[i] != 0:
    #             # 加入j个邻居到栈中
    #             for j in graph[i].keys():
    #                 # 判断是否可以激活,对每一个领点进行判断
    #                 if act_or_not[j] == False:
    #                     total_weight = get_total_activated_weight(in_degree, act_or_not, graph, j)
    #                     if total_weight >= random_list[j]:
    #                         ActivitySet.append(j)
    #                         q.append(j)
    #                         act_or_not[j] = True
    #     count = len(ActivitySet)
    #     return count
def IC_model(seeds,vertices,in_degree,out_degree,graph,in_table):
    if len(seeds)==0:
        return 0
    else :
        node_be_influenced = []
        act_or_not = {}
        for i in range(vertices):
            act_or_not[i+1] = False
        q = []
        for i in seeds:
            q.append(i)
            node_be_influenced.append(i)
            act_or_not[i] = True
        count = len(node_be_influenced)
        while len(q)!=0:
            newActivity = []
            i = q.pop()
            act_or_not[i] = True
            if out_degree[i]!=0:
                for j in graph[i].keys():
                    if act_or_not[j]==False:
                        a = random.uniform(0,1)
                        if graph[i][j]>a and act_or_not[j] == False:
                            newActivity.append(j)
                            q.append(j)
                            act_or_not[i] = True
                count = count+len(newActivity)
        return count

def ISE(social_network,seed_set,diffusion_model):
    N = 10000
    sum = 0.0
    in_table,vertices, in_degree, out_degree, direct_dict = get_graph(social_network)
    for i in range(N):
        output = diffusion_model(seed_set, vertices, in_degree, out_degree, direct_dict,in_table)
        sum = sum + output
    return sum/N
'''采用CELF算法,参考文献:http://www.doc88.com/p-3867998343720.html'''
def Real_CELF(filename,model,k,termination,budget,random_seed):
    nodes = []

    if termination == 1:
        clock = time .clock()
        in_table, vertices, in_degree, out_degree, direct_dict = get_graph(filename)
        points = []

        table = {}
        nodes_number = 1
        for i in in_degree.keys():
            points.append(i)
        for i in points:

            nodes.append(i)
            number = ISE(filename, nodes, model)
            nodes.remove(i)
            table[i] = number
        new_table = sorted(table.iteritems(), key=lambda asd: asd[1], reverse=True)
        temp = new_table
        # new_table = [(56, 44.6658), (52, 43.0), (51, 36.6013), (50, 34.3328), (58, 33.0), (53, 30.0), (62, 29.7484), (60, 28.5526), (41, 23.3517), (46, 23.1912), (44, 22.7108), (48, 22.3804), (38, 19.1979), (45, 18.3326), (43, 18.2061), (54, 16.3195), (47, 16.1402), (28, 15.1973), (31, 14.7036), (55, 14.1046), (30, 10.6183), (39, 9.5757), (34, 8.4084), (61, 8.0), (37, 7.2391), (27, 6.7726), (29, 5.912), (18, 5.5396), (42, 4.7072), (59, 4.003), (21, 3.8958), (33, 3.5769), (40, 3.5724), (25, 3.389), (36, 3.3404), (35, 3.1254), (14, 2.793), (23, 2.4515), (26, 2.4046), (32, 2.3741), (10, 1.6661), (15, 1.6606), (57, 1.656), (11, 1.5786), (20, 1.5202), (9, 1.3344), (22, 1.2496), (19, 1.2218), (17, 1.1915), (16, 1.1616), (0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0), (12, 1.0), (13, 1.0), (24, 1.0), (49, 1.0)]
        # choose a node with largest influence
        nodes.append(new_table[0][0])
        points.remove(new_table[0][0])
        new_table.remove(new_table[0])
        count = False
        # 对于剩下的节点
        while (count == False):

            # 选择影响力次大的节点
            lnode = new_table[0][0]
            nodes.append(lnode)
            number = ISE(filename, nodes, model)
            nodes.remove(lnode)
            # number1 = ISE(filename,nodes,model,0,0,0)
            # 设置标记flag
            flag = number
            sn = lnode
            for j in new_table:
                # 选择其他的结点
                if (j[0] != lnode):
                    nodes.append(j[0])
                    number = ISE(filename, nodes, model)
                    nodes.remove(j[0])
                    oz = number
                    if (flag > oz):
                        break
                    else:
                        flag = oz
                        sn = j[0]
                time1 = time.time()
                if (time1 - clock) > budget - 5:
                    nodes = get_random(temp, k)
                    break
            nodes.append(sn)
            nodes_number = nodes_number + 1

            for i in new_table:
                if i[0] == sn:
                    new_table.remove(i)
                    break
            if nodes_number == k:
                break


        return nodes
    if termination == 0:
        in_table,vertices, in_degree, out_degree, direct_dict = get_graph(filename)
        points = []

        table = {}
        nodes_number = 1
        for i in in_degree.keys():
            points.append(i)
        for i in points:
            nodes.append(i)
            number = ISE(filename,nodes,model)
            nodes.remove(i)
            table[i] = number
        new_table = sorted(table.iteritems(), key=lambda asd: asd[1], reverse=True)
        # new_table = [(56, 44.6658), (52, 43.0), (51, 36.6013), (50, 34.3328), (58, 33.0), (53, 30.0), (62, 29.7484), (60, 28.5526), (41, 23.3517), (46, 23.1912), (44, 22.7108), (48, 22.3804), (38, 19.1979), (45, 18.3326), (43, 18.2061), (54, 16.3195), (47, 16.1402), (28, 15.1973), (31, 14.7036), (55, 14.1046), (30, 10.6183), (39, 9.5757), (34, 8.4084), (61, 8.0), (37, 7.2391), (27, 6.7726), (29, 5.912), (18, 5.5396), (42, 4.7072), (59, 4.003), (21, 3.8958), (33, 3.5769), (40, 3.5724), (25, 3.389), (36, 3.3404), (35, 3.1254), (14, 2.793), (23, 2.4515), (26, 2.4046), (32, 2.3741), (10, 1.6661), (15, 1.6606), (57, 1.656), (11, 1.5786), (20, 1.5202), (9, 1.3344), (22, 1.2496), (19, 1.2218), (17, 1.1915), (16, 1.1616), (0, 1.0), (1, 1.0), (2, 1.0), (3, 1.0), (4, 1.0), (5, 1.0), (6, 1.0), (7, 1.0), (8, 1.0), (12, 1.0), (13, 1.0), (24, 1.0), (49, 1.0)]
        #choose a node with largest influence
        nodes.append(new_table[0][0])
        points.remove(new_table[0][0])
        new_table.remove(new_table[0])
        count = False
        #对于剩下的节点
        while (count==False):
            #选择影响力次大的节点
            lnode = new_table[0][0]
            nodes.append(lnode)
            number = ISE(filename,nodes,model)
            nodes.remove(lnode)
            # number1 = ISE(filename,nodes,model,0,0,0)
            #设置标记flag
            flag = number
            sn = lnode
            for j in new_table:
                #选择其他的结点
                if (j[0]!=lnode):
                    nodes.append(j[0])
                    number = ISE(filename,nodes,model)
                    nodes.remove(j[0])
                    # number1 = ISE(filename,nodes,model,0,0,0)
                    oz = number
                    if(flag>oz):
                        break
                    else:
                        flag = oz
                        sn = j[0]
            nodes.append(sn)
            nodes_number = nodes_number+1
            for i in new_table:
                if i[0]==sn:
                    new_table.remove(i)
                    break
            if nodes_number==k:
                break
        return nodes
def get_random(new_table,k):
    count = 0
    nodes = []
    for i in new_table:
        nodes.append(i[0])
        count = count+1
        if count == k:
            break
    return nodes
'''采用贪心算法'''
def normal_greedy(filename,model,k,termination,budget,random_seed):
    nodes = []
    if termination == 1:
        time1 = time.clock()
        in_table, vertices, in_degree, out_degree, direct_dict = get_graph(filename)
        points = []
        for i in in_degree.keys():
            points.append(i)
        count = 0
        while count < k:
            table = {}
            for i in points:
                # 设定出度阈值
                if out_degree[i] > 0:
                    nodes.append(i)
                    number = ISE(filename, nodes, model)
                    nodes.remove(i)
                    # number2 = ISE(filename, nodes, model)
                    table[i] = number

            new_table = sorted(table.iteritems(), key=lambda asd: asd[1], reverse=True)
            time2 = time.time()
            if time2 - time1 >= budget - 5:
                nodes = get_random(new_table,k)
                break
            nodes.append(new_table[0][0])
            points.remove(new_table[0][0])
            count = count + 1
    if termination == 0:
        in_table,vertices, in_degree, out_degree, direct_dict = get_graph(filename)
        points = []
        for i in in_degree.keys():
            points.append(i)

        count = 0
        while count<k:
            table = {}
            for i in points:
                #设定出度阈值
                if out_degree[i]>0:
                    nodes.append(i)
                    number = ISE(filename, nodes, model)
                    nodes.remove(i)
                    number2 = ISE(filename, nodes, model)
                    table[i] = number-number2
            new_table = sorted(table.iteritems(), key=lambda asd: asd[1], reverse=True)
            nodes.append(new_table[0][0])
            points.remove(new_table[0][0])
            count = count+1
    return nodes
if __name__ == "__main__":
    time1 = time.time()
    nodes = Real_CELF("network.txt", LT_model, 4,0,10,0)
    time2 = time.time()
    print  nodes
