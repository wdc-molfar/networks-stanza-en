# graphprocessing.py

import networkx as nx
from networkx.readwrite import json_graph

def remove_loops(DWNT):
    # renove loops
    try:
        for i in DWNT.nodes():
            if DWNT.get_edge_data(i, i, default=0) != 0:
                DWNT.remove_edge(i, i)
    except:   
        print ("DWNT has no nodes")
    return DWNT


def remove_edges(DWNT):
    #remove edges that have weight equal 1
    try:
        for i in DWNT.nodes():
            for j in DWNT.nodes():
                if DWNT.get_edge_data(i, j, default=0) != 0:
                    if DWNT.get_edge_data(i, j, default=0).get('weight') == 1:
                        DWNT.remove_edge(i, j)
    except:
        print ("DWNT has no edges")
    return DWNT

def remove_nodes(DWNT):
    #remove nodes that have no connections
    try:
        degrees = dict(DWNT.degree())
        for i in degrees:
            if degrees.get(i) == 0:
                DWNT.remove_node(i)
    except:
        print ("DWNT has no nodes")
    return DWNT


def graph_preprocessing(DWNT):
    DWNT = remove_loops(DWNT)
    DWNT = remove_edges(DWNT)
    DWNT = remove_nodes(DWNT)
    return DWNT

def network_graphml(DWNT):
    #converting to json format
    DWNT = graph_preprocessing(DWNT)
    nx.write_graphml(DWNT,'DWNT.graphml')
    return
    
def network_json(DWNT):
    #converting to json format
    DWNT = graph_preprocessing(DWNT)
    jsn = json_graph.node_link_data(DWNT)
    del jsn['directed']
    del jsn['multigraph']
    del jsn['graph']
    return str(jsn)
    