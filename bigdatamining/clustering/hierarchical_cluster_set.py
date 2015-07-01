import gzip
import json
import numpy
import operator
import sys
####################################################################################
#
#   Correlation defined as set
#   Heuristical clustering based on jaccard
#
#   Example: python heuristical_cluster_set.py [threshold]  #threshold is a numbe between [0, 1] default 0.1
#
####################################################################################



debug = True

#heuristics constant
#also_bought weight
alpha = 0.5
#also viewed weight
beta = 0.2
#bought togheter
gamma = 1.0

def get_data(path):
    file = gzip.open(path, 'r')
    count = 0
    
    clusters = {}
    dict = {}
    
    for line in file:
        parsedline = json.loads(line)
        if 'asin' in parsedline: #ASIN not exists or already in dict, don't do
            main_index = count
            clusters[parsedline['asin']] = main_index
            dict[main_index] = []
            count += 1
            if 'related' in parsedline:
                if 'also_bought' in parsedline['related']:
                    for item in parsedline['related']['also_bought']:
                            dict[main_index].append(item)
                if 'also_viewed' in parsedline['related']:
                    for item in parsedline['related']['also_viewed']:
                            dict[main_index].append(item)
                if 'bought_together' in parsedline['related']:
                    for item in parsedline['related']['bought_together']:
                            dict[main_index].append(item)
    #delete duplicates and get sets
    for k,v in dict.iteritems():
        dict[k] = [set(dict[k])]
    file.close()
    return dict, clusters, count


def init_matrix(sets, n_items):
    distance_matrix = numpy.zeros((n_items, n_items))
    
    for k1,v1 in sets.iteritems():
        for k2,v2 in sets.iteritems():
            distance_matrix[k1][k2] = jaccard_coefficient(v1[0],v2[0])
    distance_matrix = numpy.triu(distance_matrix, +1)
    #numpy.savetxt('test.txt', distance_matrix)
    return distance_matrix

def find_clusters_to_merge(clusters, distance_matrix, n_items):
    #find index of max value in matrix
    index = numpy.argmax(distance_matrix)
    n_row = round(index / n_items)
    n_col = index % n_items
    return n_row, n_col

def merge_clusters(clusters, distance_matrix, n_row, n_col):
    #we use always the n_row as new index
    #first delete the weights between them
    distance_matrix[n_row][n_col] = 0
    #update values
    for i in range(len(distance_matrix[0])):
        if  n_row < i :
            distance_matrix[n_row][i] = (distance_matrix[n_row][i] + max(distance_matrix[n_col][i], distance_matrix[i][n_col]))/2
        elif n_row > i:
            distance_matrix[i][n_row] = (distance_matrix[i][n_row] + max(distance_matrix[i][n_col], distance_matrix[n_col][i]))/2
        distance_matrix[i][n_col] = 0
        distance_matrix[n_col][i] = 0

    #update clusters
    for key, value in clusters.iteritems():
        if value == n_col:
            clusters[key] = n_row

    return clusters, distance_matrix


def hierarchical_clustering_set(clusters, distance_matrix, n_items, threshold):
    max = 1
    while(max > threshold):
        #find clusters to merge
        n_row, n_col = find_clusters_to_merge(clusters, distance_matrix, n_items)
        max = distance_matrix[n_row][n_col]
        #so we need to merge clusters n_row and n_col
        clusters, distance_matrix = merge_clusters(clusters, distance_matrix, n_row, n_col)

    result = {}
    #group cluster's items
    for key,value in clusters.iteritems():
        if value not in result:
            result[value] = [key]
        else:
            result[value].append(key)

    return result


# Compute the Jaccard coefficient between two sets
def jaccard_coefficient (d1, d2):
    if (len(d1) + len(d2)) == 0:
        return 0.0
    intersection_size = len (d1 & d2)
    return float(intersection_size) / (len(d1) + len(d2) - intersection_size)

def get_recommendation(set_clusters, asin, n_recommendation):
    #find the cluster of the asin item
    cluster_id = -1
    for key, value in set_clusters.iteritems():
        if asin in value:
            cluster_id = key
            break

    if cluster_id == -1:
        return -1
    else:
        #filter the list so i don0t return myself
        temp = filter(lambda x: x != asin, set_clusters[cluster_id])
        return temp[:n_recommendation]

if __name__ == '__main__':
    
    threshold = 0.1 if len(sys.argv) < 2 else sys.argv[1]
    
    if debug:
        sets, clusters, n_items = get_data("5k.json.gz")
    else:
        sets, clusters, n_items = get_data("meta_Grocery_and_Gourmet_Food.json.gz")

    distance_matrix = init_matrix(sets, n_items)
    print "Matrix initialized"
    result = hierarchical_clustering_set(clusters, distance_matrix, n_items, threshold)

    for k,v in result.iteritems():
        print "Cluster: " + str(k) + " contains: " + str(v)











