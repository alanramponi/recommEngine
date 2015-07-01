import gzip
import json
import numpy
import operator
import hashlib
import time
import datetime
####################################################################################
#
#   Correlation defined with alpha, beta and gamma.
#   Heuristical clustering with dictionaries
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
    set = gzip.open(path, 'r')
    count = 0
    
    clusters = {}
    dict = {}
    
    for line in set:
        parsedline = json.loads(line)
        if 'asin' in parsedline: #ASIN not exists or already in dict, don't do
            main_index = count
            clusters[parsedline['asin']] = main_index
            dict[main_index] = []
            count += 1
            if 'related' in parsedline:
                if 'also_bought' in parsedline['related']:
                    for item in parsedline['related']['also_bought']:
                            dict[main_index].append((item, alpha))
                if 'also_viewed' in parsedline['related']:
                    for item in parsedline['related']['also_viewed']:
                            dict[main_index].append((item, beta))
                if 'bought_together' in parsedline['related']:
                    for item in parsedline['related']['bought_together']:
                            dict[main_index].append((item, alpha))
    set.close()

    for k, val in dict.iteritems():
        temp = []
        for i in range(len(val)):
            if val[i][0] in clusters:
                temp.append(val[i])
        dict[k] = temp

    return clusters, dict, len(dict)

def init_matrix(clusters, dict, n_items):
    
    distance_matrix = numpy.zeros((n_items, n_items))

    for k,dk in dict.iteritems():
        for i in range(len(dk)):
            distance_matrix[k][clusters[dk[i][0]]] += dk[i][1]

    #i need only the upper triangle of the matrix
    distance_matrix = distance_matrix + distance_matrix.transpose()
    distance_matrix = numpy.triu(distance_matrix, +1)
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


def hierarchical_clustering(clusters, distance_matrix, n_items):
    count = 0
    max = 1
    while(max > 0.00000005):
        n_row, n_col = find_clusters_to_merge(clusters, distance_matrix, n_items)
        max = distance_matrix[n_row][n_col]
        #so we need to merge clusters n_row and n_col
        clusters, distance_matrix = merge_clusters(clusters, distance_matrix, n_row, n_col)
        count += 1

    result = {}
    #group cluster's items
    for key,value in clusters.iteritems():
        if value not in result:
            result[value] = [key]
        else:
            result[value].append(key)

    return result

def get_recommendation(hierarical_clusters, asin, n_recommendation):
    #find cluster
    cluster_id = -1
    for key, value in hierarical_clusters.iteritems():
        if asin in value:
            cluster_id = key
            break

    if cluster_id == -1:
        return -1
    else:
        #filter the list so i don0t return myself
        temp = filter(lambda x: x != asin, hierarical_clusters[cluster_id])
        return temp[:n_recommendation]


if __name__ == '__main__':
    ts = datetime.datetime.now()
    if debug:
        clusters, data, n_items = get_data("500.json.gz")
    #data, clusters = init_vectors("meta_Grocery_and_Gourmet_Food.json.gz")
    else:
        data, clusters = init_vectors("meta_Grocery_and_Gourmet_Food.json.gz")

    distance_matrix = init_matrix(clusters, data, n_items)
    print "Matrix initialized"
    result = hierarchical_clustering(clusters, distance_matrix, n_items)

    #print result
    for key, value in result.iteritems():
        print str(key) + "  " + str(value)









