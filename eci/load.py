# -*- coding: UTF-8 -*-
import networkx as nx
import csv

conuts = 0

def load_data(path):
    G = nx.Graph()
    global conuts
    with open(path) as f:
        f_csv = csv.reader(f)
        conuts = sum(1 for row in f_csv)

    # G.add_nodes_from(_load_nodes(path))
    return _load_edge(path,G)

def _load_nodes(path):
    nodes = list()
    with open(path) as f:
        f_csv = csv.reader(f)
        _now = 0
        for row in f_csv:
            _now += 1
            print "%s : %d / %d" % ("load_node", _now, conuts)
            if row[0] not in nodes:
                nodes.append(row[0])
            if row[1] not in nodes:
                nodes.append(row[1])
    return nodes


def _load_edge(path,g):
    with open(path) as f:
        f_csv = csv.reader(f)
        _now = 0
        for row in f_csv:
            _now += 1
            print "%s : %d / %d" % ("load_node", _now, conuts)
            g.add_edge(row[0],row[1])
    return g