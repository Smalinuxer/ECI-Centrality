# -*- coding: UTF-8 -*-
import math
import time
import networkx as nx

def Collective_Influence(G,d):
    node_set = G.nodes()
    count = 0
    all_counts = len(node_set)

    Collective_Influence_Collects = dict()
    for nid in node_set:
        Interior_Center_set = []
        Center_set = [nid]  # 关键层
        Neighbor_set = []
        for i in range(0, d):

            for center in Center_set:
                Neighbor_set = list(set(Neighbor_set).union(G.neighbors(center)))
                # print "neighbors:", center, Neighbor_set, G.neighbors(center)

            # 更新源和邻居集合
            # 从当前层的邻居节点集合中删除内层节点和本层节点，获得外层节点集合
            Temp_Set = list(set(list(set(Neighbor_set).difference(set(Interior_Center_set)))).difference(set(Center_set)))
            Interior_Center_set = Center_set
            Center_set = Temp_Set
            Neighbor_set = []

        Total_Reduced_Degree = 0.0
        for id in Center_set:
            Total_Reduced_Degree = Total_Reduced_Degree + (G.degree(id) - 1.0)

        Collective_Influence = (G.degree(nid) - 1.0) * Total_Reduced_Degree
        Collective_Influence_Collects[nid] = Collective_Influence
        count += 1
        print "%d / %d" % (count, all_counts)

    return Collective_Influence_Collects

def Enhanced_Collective_Influence_Native(G, d):
    #强化的Collective Influence, 参数d为考虑的范围radius。
    Enhanced_Collective_Influence_Dic = {}
    node_set = G.nodes()
    count = 0
    all_counts = len(node_set)
    for nid in node_set: #对于网路中每个节点, 返回Center_set为距离中心节点 “d层”的节点集合。

        time1 = time.time()

        #循环过程的初始源和邻居
        Interior_Center_set = []
        Center_set = [nid] #关键层
        Neighbor_set = []
        #print nid, Center_set, d
        for i in range(0, d):


            for center in Center_set:
                Neighbor_set = list(set(Neighbor_set).union(G.neighbors(center)))
                #print "neighbors:", center, Neighbor_set, G.neighbors(center)
            #end for

            #更新源和邻居集合
            #从当前层的邻居节点集合中删除内层节点和本层节点，获得外层节点集合
            Temp_Set = list(set(list(set(Neighbor_set).difference(set(Interior_Center_set)))).difference(set(Center_set)))
            Interior_Center_set = Center_set
            Center_set = Temp_Set
            Neighbor_set = []
        #end for

        time2 = time.time()

        #(1)计算Collective_Influence取值
        Total_Reduced_Degree = 0.0
        for id in Center_set:
            Total_Reduced_Degree = Total_Reduced_Degree + (G.degree(id)-1.0)

        Collective_Influence = (G.degree(nid)-1.0) * Total_Reduced_Degree

        time3 = time.time()

        #(2)对nid的Collective_Influence进行关于Structure division(Hole spanners)的检测强化
        Associations_Ngb_Area_2 = 0
        for id1 in Center_set: #Center_set：离中心源点不同层的节点集合
            for id2 in Center_set:
                if id1 != id2:
                    NGB1 = list(set(G.neighbors(id1)).difference(set([nid])))
                    NGB1.append(id1)
                    NGB2 = list(set(G.neighbors(id2)).difference(set([nid])))
                    #NGB2.append(id2)
                    #print NGB2, NGB2, set(NGB1).intersection(set(NGB2))
                    Associations_Ngb_Area_2 = Associations_Ngb_Area_2 + len(set(NGB1).intersection(set(NGB2)))
                    #print "xijie", nid, Center_set, id1, id2, NGB1, NGB2, len(set(NGB1).intersection(set(NGB2)))

        Associations_Ngb_Area_1 = 0
        if len(Interior_Center_set) > 1:
            for id1 in Interior_Center_set: #Center_set：离中心源点不同层的节点集合
                for id2 in Interior_Center_set:
                    if id1 != id2:
                        NGB1 = list(set(G.neighbors(id1)).difference(set([nid])))
                        NGB1.append(id1)
                        NGB2 = list(set(G.neighbors(id2)).difference(set([nid])))
                        Associations_Ngb_Area_1 = Associations_Ngb_Area_1 + len(set(NGB1).intersection(set(NGB2)))


        time4 = time.time()

        #(3)节点nid的邻居结构的均衡性-structural entropy
        Degree_List = []
        Total_Degree = 0
        for node in G.neighbors(nid):
            Degree_List.append(G.degree(node))
            Total_Degree = Total_Degree + G.degree(node)
        #end for
        #print nid, Degree_List
        for i in range(0,len(Degree_List)):
            Degree_List[i] = Degree_List[i]/float(Total_Degree)

        time5 = time.time()

        #计算熵
        Entropy = 0.0
        for i in range(0,len(Degree_List)):
            #print " Degree_List[i]:",  Degree_List[i]
            Entropy = Entropy + ( - Degree_List[i] * math.log( Degree_List[i] ) + 0.1 )
        #print G.degree(nid)
        Entropy = Entropy / math.log( G.degree(nid) + 0.1 )

        #计算Enhanced_Collective_Influence
        #Enhanced_Collective_Influence_Dic[nid] = [Collective_Influence / ((Associations_Ngb_Area_1+Associations_Ngb_Area_2)/2.0 + 0.001), Entropy]  # [Collective_Influence, Associations_Ngb_Area/2]
        Enhanced_Collective_Influence_Dic[nid] = Entropy * Collective_Influence / ((Associations_Ngb_Area_1 + Associations_Ngb_Area_2) / 2.0 + 0.001)  # [Collective_Influence, Associations_Ngb_Area/2]

        time6 = time.time()

        count += 1
        print "%d / %d" % (count , all_counts)

        print "time2 - time1 : %d " % (time2 - time1)
        print "time3 - time2 : %d " % (time3 - time2)
        print "time4 - time3 : %d " % (time4 - time3)
        print "time5 - time4 : %d " % (time5 - time4)
        print "time6 - time5 : %d " % (time6 - time5)
        #print "nid:",nid,t2-t1
    #end for

    return Enhanced_Collective_Influence_Dic



def Enhanced_Collective_Influence(G, d=2):
    #强化的Collective Influence, 参数d为考虑的范围radius。
    Enhanced_Collective_Influence_Dic = {}

    node_set = G.nodes()
    count = 0
    all_counts = len(node_set)
    #对于网路中每个节点。
    for nid in node_set:
        neighbor_hop_1 = G.neighbors(nid)
        neighbor_hop_2 = []
        for ngb1 in neighbor_hop_1:
            neighbor_hop_2 = list(set(neighbor_hop_2).union(G.neighbors(ngb1)))
        #end for
        neighbor_hop_2 = list(  set(neighbor_hop_2).difference( set(neighbor_hop_1).union(set([nid]))  ) )

        #(1)计算Collective_Influence取值
        Total_Reduced_Degree = 0.0
        for id in neighbor_hop_2:
            Total_Reduced_Degree = Total_Reduced_Degree + (G.degree(id)-1.0)
        #end
        Collective_Influence = (G.degree(nid)-1.0) * Total_Reduced_Degree

        #(2)对nid的Collective_Influence进行关于neighbors的Correlation_Intensity强化

        Correlation_Intensity = 0.0

        for id1 in neighbor_hop_2: #Center_set：离中心源点不同层的节点集合
            for id2 in neighbor_hop_2:
                if id1 != id2:
                    Correlation_Intensity = Correlation_Intensity + float(len(set(G.neighbors(id1)).intersection(set(G.neighbors(id2))))) / float(len(set(G.neighbors(id1)).union(set(G.neighbors(id2)))))
        #end for

        Correlation_Intensity_1 = 0.0
        for id1 in neighbor_hop_1: #Center_set：离中心源点不同层的节点集合
            for id2 in neighbor_hop_1:
                if id1 != id2:
                    Correlation_Intensity_1 = Correlation_Intensity_1 + float(len(set(G.neighbors(id1)).intersection( set(G.neighbors(id2)).difference(set([nid]))  ))) / float(len(set(G.neighbors(id1)).union(  set(G.neighbors(id2)).difference(set([nid]))   )))
        #end for
        Correlation_Intensity = 0.5*Correlation_Intensity + Correlation_Intensity_1

        '''
        #SubG_1 = G.subgraph(neighbor_hop_1).copy() #子图
        SubG_2 = G.subgraph(neighbor_hop_2).copy() #子图
        #SubEdge_1 = SubG_1.number_of_edges()
        SubEdge_2 = SubG_2.number_of_edges()
        #SubDegree_1 = sum(G.degree(v) for v in SubG_1.nodes())
        SubDegree_2 = sum(G.degree(v) for v in SubG_2.nodes())
        #Correlation_Intensity = 2*float(SubEdge_1)/(SubDegree_1+1) + float(SubEdge_2)/(SubDegree_2+1)
        Correlation_Intensity = Correlation_Intensity + float(SubEdge_2)/(SubDegree_2+1)
        '''


        #(3)计算邻居结构的均衡性-structural entropy
        #邻居节点的度概率-Degree proporational list
        Degree_List = []
        Total_Degree = 0
        for node in G.neighbors(nid):
            Degree_List.append(G.degree(node))
            Total_Degree = Total_Degree + G.degree(node)
        #end for
        for i in range(0,len(Degree_List)):
            Degree_List[i] = Degree_List[i]/float(Total_Degree)
        #end for
        #计算正则化熵
        Entropy = 0.0
        for i in range(0, len(Degree_List)):
            Entropy = Entropy + ( - Degree_List[i] * math.log( Degree_List[i] ) )
        Entropy = Entropy / math.log( G.degree(nid) + 0.1 )
        #end for

        #（4）计算Enhanced_Collective_Influence(ECI)
        Enhanced_Collective_Influence_Dic[nid] = Collective_Influence * Entropy/(1+Correlation_Intensity)
        count += 1
        print "%d / %d" % (count, all_counts)
    #end for

    #print sorted(Enhanced_Collective_Influence_Dic.iteritems(), key=lambda d:d[1], reverse = True)
    return Enhanced_Collective_Influence_Dic
