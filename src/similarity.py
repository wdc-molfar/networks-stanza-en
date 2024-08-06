# similarity.py

import networkx as nx
import numpy as np
import json


def frobenius(network1, network2):
    network1 = json.loads(network1.replace("\'", "\""))
    network2 = json.loads(network2.replace("\'", "\""))

    # Returns graph from node-link data format
    network1 = nx.node_link_graph(network1)
    network2 = nx.node_link_graph(network2)

    # Return the graph adjacency matrix as a NumPy matrix
    matrix1 = nx.to_numpy_array(network1)
    matrix2 = nx.to_numpy_array(network2)
    a = matrix1 - matrix2

    # summa = 0
    # for row in a:
    #    for el in np.array(row)[0]:
    #        summa = summa + (el*el)

    # matrx[i][j] = np.sqrt(summa)
    similarity = 1 - np.linalg.norm(a, 'fro')

    return similarity