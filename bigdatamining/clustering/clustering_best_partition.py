import networkx as nx
import random
import gzip
import json
import community
import matplotlib.pyplot as plt
import operator
import time

########################################################################################
#
#   Communit detection on graph (Last version)
#
########################################################################################

debug = False

def create_graph(path):
    #heuristics constant
    #also_bought weight
    alpha = 0.3
    #also viewed weight
    beta = 0.1
    #bought togheter
    gamma = 1.0
    
    set = gzip.open(path, 'r')
    
    G = nx.Graph()
    
    for line in set:
        
        parsedline = json.loads(line)
        try:
            
            if 'asin' in parsedline: #ASIN not exists or already in dict, don't do
                new_node = parsedline['asin']
                if new_node not in G:
                    G.add_node(new_node)
                if 'related' in parsedline:
                    if 'also_bought' in parsedline['related']:
                        for item in parsedline['related']['also_bought']:
                            if G.has_edge(new_node, item):
                                G[new_node][item]['weight'] = G[new_node][item]['weight'] + alpha
                            else:
                                G.add_edge(new_node, item, weight=alpha)
                    if 'also_viewed' in parsedline['related']:
                        for item in parsedline['related']['also_viewed']:
                            if G.has_edge(new_node, item):
                                G[new_node][item]['weight'] = G[new_node][item]['weight'] + beta
                            else:
                                G.add_edge(new_node, item, weight=beta)
                    if 'bought_together' in parsedline['related']:
                        for item in parsedline['related']['bought_together']:
                            if G.has_edge(new_node, item):
                                G[new_node][item]['weight'] = G[new_node][item]['weight'] + gamma
                            else:
                                G.add_edge(new_node, item, weight=gamma)
    
        except (RuntimeError, TypeError, NameError):
            print "EXCEPTION: error"

    set.close()
    return G

def plot_graph(G, partition):
    #drawing
    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()) :
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20, node_color = str(count / size))
    nx.draw_networkx_edges(G,pos, alpha=0.5)
    plt.show()

def print_to_file(sorted_partition):
    #time for different name of result file
    ts = time.time()
    last = -1
    f = open('results_' + str(ts) + '.txt', 'w')
    for tupla in sorted_partition:
        if last != tupla[1]:
            f.write ('\n Value:' + str(tupla[1]) + '  ')
            last = tupla[1]
        f.write (str(tupla[0]) + '  ')
    f.close()


def cluster_graph(G):
    #first compute the best partition
    partition = community.best_partition(G)
    sorted_partition = sorted(partition.items(), key=operator.itemgetter(1))
    return sorted_partition

def check_target_and_find_cluster(asin, clusters):
    #find cluster id, if I can't find it return None
    for i in range(len(clusters)):
        if clusters[i][0] == asin:
            return clusters[i][1]
    return None
    

def recommender(clusters, cluster_id, asin, n_recommendation=10):
    #filter clusters to get only my cluster
    my_cluster = []
    i = 0
    while i < len(clusters) and clusters[i][1]<= cluster_id:  #is ordered
        if clusters[i][1] == cluster_id and clusters[i][0] != asin:
            my_cluster.append(clusters[i][0])
        i += 1
    #TODO: how can we select the best matching in the cluster? for now random
    return my_cluster[:n_recommendation]



if __name__ == '__main__':

    if debug:
        G = create_graph("test_case.json.gz")
    else:
        G = create_graph("meta_Grocery_and_Gourmet_Food.json.gz")
        #G = create_graph("meta_Books.json.gz")


    #first compute the best partition
    partition = community.best_partition(G)
    sorted_partition = sorted(partition.items(), key=operator.itemgetter(1))
    print_to_file(sorted_partition)


