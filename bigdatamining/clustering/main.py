import sys
import time

import clustering_best_partition as cbp
#import hierarchical_cluster_v2 as hc
import hierarchical_cluster_v3 as hc
import hierarchical_cluster_set as hs


#############################################################
#
#   All togeter NOW!!!!
#
#   Example:
#   python main.py  #(if you want the default dataset)
#   python main.py dataset_path_.json.gz #(to select your dataset)
#
#############################################################

#############################################################

debug = False

default_path = "../../data/500_meta.json.gz"

#get IDF thrashold if one
path = default_path if len(sys.argv) < 2 else sys.argv[1]
n_recommendation = 5  #number of recommendation given by the algo

#############################################################
#ask for the target item:
asin = raw_input("Please enter an item ASIN (e.g. B0000CDBQT or B0000AE5Z7): ")

#############################################################
#Import dataset and build the graph
print "Eval Graph Partition"
start = time.time()
G = cbp.create_graph(path)

#############################################################
#clustering of the graph with best partiotion algorithm

graph = cbp.cluster_graph(G)

cluster_id = cbp.check_target_and_find_cluster(asin, graph)

# Error if the targeted ASIN is not found
if cluster_id == None:
    sys.exit('*** FATAL *** item not found')

#############################################################
#Best partition clustering
#optional params number of recommendation (default 5)
partiotion_based_reccomandation = cbp.recommender(graph, cluster_id, asin, n_recommendation)
end = time.time()
print "in " + str(end - start) + " seconds"
#############################################################
#Hierarchical clustering based on weighted relationship
print "Eval Hierarchical Clustering"
start = time.time()
clusters, data, n_items = hc.get_data(path)
distance_matrix = hc.init_matrix(clusters, data, n_items)
hierarical_clusters = hc.hierarchical_clustering(clusters, distance_matrix, n_items)
hierarical_based_recommendation = hc.get_recommendation(hierarical_clusters, asin, n_recommendation)

end = time.time()
print "in " + str(end - start) + " seconds"

#############################################################
print "Eval Set Clustering"
start = time.time()
#hierarchical clustering based on sets
threshold = 0.1  #Heuristical threshold for jaccard similarity
sets, clusters, n_items = hs.get_data(path)
distance_matrix = hs.init_matrix(sets, n_items)
set_clusters = hs.hierarchical_clustering_set(clusters, distance_matrix, n_items, threshold)
sets_based_recommendation = hs.get_recommendation(set_clusters, asin, n_recommendation)
if sets_based_recommendation == -1:
    sys.exit('*** FATAL *** Item not found in the sets')

end = time.time()
print "in " + str(end - start) + " seconds"

######################################################################

#print results for desired item
partition_result = []
hierarical_result = []
sets_result = []
#format output to print (remember cluster not ensured to be at least n_recommendation long)
for i in range(n_recommendation):
    if i < len(partiotion_based_reccomandation):
        partition_result.append(partiotion_based_reccomandation[i])
    else:
        partition_result.append("##########")
    if i < len(hierarical_based_recommendation):
        hierarical_result.append(hierarical_based_recommendation[i])
    else:
        hierarical_result.append("##########")
    if i < len(sets_based_recommendation):
        sets_result.append(sets_based_recommendation[i])
    else:
        sets_result.append("##########")

print 'Resulting top rankings:\nGraph Based\tWeight Based\tSets Based'
for i in range(n_recommendation):
    print '%s\t%s\t%s' % (
                          partition_result[i],
                          hierarical_result[i],
                          sets_result[i])


#FOR DEBUG PURPOSE
while(True and debug):
    #ask for the target item:
    asin = raw_input("Please enter an item ASIN (e.g. B0000AE5Z7 or B0000AE5Z7): ")

    cluster_id = cbp.check_target_and_find_cluster(asin, graph)

    # Error if the targeted ASIN is not found
    if cluster_id == None:
        sys.exit('*** FATAL *** item not found')
    partiotion_based_reccomandation = cbp.recommender(graph, cluster_id, asin, n_recommendation)
    hierarical_based_recommendation = hc.get_recommendation(hierarical_clusters, asin, n_recommendation)
    sets_based_recommendation = hs.get_recommendation(set_clusters, asin, n_recommendation)

    #print results for desired item
    partition_result = []
    hierarical_result = []
    sets_result = []
    #format output to print (remember cluster not ensured to be at least n_recommendation long)
    for i in range(n_recommendation):
        if i < len(partiotion_based_reccomandation):
            partition_result.append(partiotion_based_reccomandation[i])
        else:
            partition_result.append("##########")
        if i < len(hierarical_based_recommendation):
            hierarical_result.append(hierarical_based_recommendation[i])
        else:
            hierarical_result.append("##########")
        if i < len(sets_based_recommendation):
            sets_result.append(sets_based_recommendation[i])
        else:
            sets_result.append("##########")

    print 'Resulting top rankings:\nGraph Based\tWeight Based\tSets Based'
    for i in range(n_recommendation):
        print '%s\t%s\t%s' % (
                          partition_result[i],
                          hierarical_result[i],
                          sets_result[i])


# 1453060375 buono primi 2
# 1453060782 buono primi due
# B0000CDBQT buono su tutti
# B0000AE5Z7 buono su tutti



