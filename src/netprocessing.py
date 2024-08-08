# netprocessing.py

import networkx as nx
from networkx.readwrite import json_graph
import json


def remove_loops(DWNT):
    # renove loops
    try:
        for i in DWNT.nodes():
            if DWNT.get_edge_data(i, i, default=0) != 0:
                DWNT.remove_edge(i, i)
    except:
        print("DWNT has no nodes")
    return DWNT


def remove_edges(DWNT):
    # remove edges that have weight equal 1
    try:
        for i in DWNT.nodes():
            for j in DWNT.nodes():
                if DWNT.get_edge_data(i, j, default=0) != 0:
                    if DWNT.get_edge_data(i, j, default=0).get('weight') == 1:
                        DWNT.remove_edge(i, j)
    except:
        print("DWNT has no edges")
    return DWNT


def remove_nodes(DWNT):
    # remove nodes that have no connections
    try:
        degrees = dict(DWNT.degree())
        for i in degrees:
            if degrees.get(i) == 0:
                DWNT.remove_node(i)
    except:
        print("DWNT has no nodes")
    return DWNT


def graph_preprocessing(DWNT):
    DWNT = remove_loops(DWNT)
    DWNT = remove_edges(DWNT)
    DWNT = remove_nodes(DWNT)
    return DWNT


def network_graphml(DWNT):
    # converting to json format
    DWNT = graph_preprocessing(DWNT)
    nx.write_graphml(DWNT, 'DWNT.graphml')
    return


def network_json(DWNT):
    # converting to json format
    DWNT = graph_preprocessing(DWNT)
    jsn = json_graph.node_link_data(DWNT)
    del jsn['directed']
    del jsn['multigraph']
    del jsn['graph']
    return str(jsn)


# Return the graph adjacency matrix as a NumPy matrix
def network_to_matrix(nx_network, nodelist):
    matrix = nx.to_numpy_array(nx_network, nodelist = nodelist)
    return matrix


# Convert JSON to networkx
def json_to_network(json_network):
    json_network = json.loads(json_network.replace("\'", "\""))

    # Returns graph from node-link data format
    nx_network = nx.node_link_graph(json_network)

    return nx_network
