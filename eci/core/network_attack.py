#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module implements dynamic processes.
"""
import linecache
import string
import os
import math
import time
import networkx as nx



def Optimal_Percolation_Simultaneous_Attack(G, Centrality):
    Gn = G.copy()
    Ranking = Ranking_methods.Nodes_Ranking(Gn, Centrality)
    Ranking = sorted(Ranking.iteritems(), key=lambda d:d[1], reverse = True)

    Giant_Component_Size_List = []
    Component_Num_List = []
    for nid in Ranking:
        G.remove_node(nid[0])
        Components = sorted(nx.connected_components(G), key = len, reverse=True)
        if len(Components) >= 1:
            Giant_Component_Size = len(Components[0])
            if Giant_Component_Size > 1:
                Giant_Component_Size_List.append(Giant_Component_Size)
                Component_Num_List.append(len(Components))

    return Giant_Component_Size_List,Component_Num_List

def Optimal_Percolation_Sequence_Attack(G, Centrality, r=0.025):
    print "Optimal_Percolation_Sequence_Attack"
    Step = int(r*G.number_of_nodes())
    print Step
    Gn = G.copy()
    Ranking = Ranking_methods.Nodes_Ranking(Gn, Centrality)
    Ranking = sorted(Ranking.iteritems(), key=lambda d:d[1], reverse = True)
    G.remove_node(Ranking[0][0])

    Giant_Component_Size_List = []
    Components = sorted(nx.connected_components(G), key = len, reverse=True)
    Giant_Component_Size = len(Components[0])
    Giant_Component_Size_List.append(Giant_Component_Size)

    while Giant_Component_Size_List[-1] > 2 and Ranking != {}:
        Gn = G.copy()
        Ranking = Ranking_methods.Nodes_Ranking(Gn, Centrality)
        Ranking = sorted(Ranking.iteritems(), key=lambda d:d[1], reverse = True)
        if len(Ranking) > Step:
            for i in range(0,Step):
                G.remove_node(Ranking[i][0])
        Components = sorted(nx.connected_components(G), key = len, reverse=True)
        Giant_Component_Size = len(Components[0])
        Giant_Component_Size_List.append(Giant_Component_Size)


    return Giant_Component_Size_List





