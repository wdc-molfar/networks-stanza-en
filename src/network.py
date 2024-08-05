# network.py

import networkx as nx

def horizontal_visibility_graph(g, tseries, sentTuples, k):
    if len(sentTuples)==0:
        return g, k
    if len(sentTuples)==1:
        tseries.append( (k, sentTuples[0][2]) )
        g.add_node(sentTuples[0][0], term = sentTuples[0][0], tag = sentTuples[0][1], mag = sentTuples[0][2])
        k+=1
        return g, k
    # convert list of magnitudes into list of tuples that hold the index  
    for t in range(len(sentTuples)):
        tseries.append( (k, sentTuples[t][2]) )
        g.add_node(sentTuples[t][0], term = sentTuples[t][0], tag = sentTuples[t][1], mag = sentTuples[t][2])
        k += 1
        
    for i in range(len(sentTuples)-1):
        for j in range(i+1, len(sentTuples)):
            (ti, yi) = tseries[i]
            (tj, yj) = tseries[j]
            if (yj>=yi):
                if ((sentTuples[j][0]).count(sentTuples[i][0]) != 0) and ((sentTuples[i][1]).count('~') < (sentTuples[j][1]).count('~')):
                    if (g.get_edge_data(sentTuples[ti][0], sentTuples[tj][0], default=0) != 0):
                        g.add_edge(sentTuples[ti][0], sentTuples[tj][0], 
                                   weight = g[sentTuples[ti][0]][sentTuples[tj][0]]['weight']+1)
                        break
                    else:
                        g.add_edge(sentTuples[ti][0], sentTuples[tj][0], weight = 1)
                        break  
                elif ((sentTuples[i][0]).count(sentTuples[j][0]) != 0) and ((sentTuples[j][1]).count('~') < (sentTuples[i][1]).count('~')):
                    if (g.get_edge_data(sentTuples[tj][0], sentTuples[ti][0], default=0) != 0):
                        g.add_edge(sentTuples[tj][0], sentTuples[ti][0], 
                                   weight = g[sentTuples[tj][0]][sentTuples[ti][0]]['weight']+1)
                        break
                    else:
                        g.add_edge(sentTuples[tj][0], sentTuples[ti][0], weight = 1)
                        break
                elif (g.get_edge_data(sentTuples[ti][0], sentTuples[tj][0], default=0) != 0):
                    g.add_edge(sentTuples[ti][0], sentTuples[tj][0], 
                               weight = g[sentTuples[ti][0]][sentTuples[tj][0]]['weight']+1)
                    break
                else:
                    g.add_edge(sentTuples[ti][0], sentTuples[tj][0], weight = 1)
                    break                  
    i = len(sentTuples)-1
    j = i-1
    while i != 0:
        while j >= 0:
            (ti, yi) = tseries[i]
            (tj, yj) = tseries[j]
            if (yj>yi):     
                if (g.get_edge_data(sentTuples[tj][0], sentTuples[ti][0], default=0) != 0):
                    g.add_edge(sentTuples[tj][0], sentTuples[ti][0],
                               weight = g[sentTuples[tj][0]][sentTuples[ti][0]]['weight']+1)
                    break
                else:
                    g.add_edge(sentTuples[tj][0], sentTuples[ti][0], weight = 1)
                    break
            j -= 1
        i -= 1
        j = i-1  
    return g, k

def directed_weighted_network_terms(sentsTuples):
    dwnt = nx.DiGraph()
    n = 0
    tseries = []
    for t in range(len(sentsTuples)):
        DWNT, n = horizontal_visibility_graph(dwnt, tseries, sentsTuples[t], n)
    return dwnt
        