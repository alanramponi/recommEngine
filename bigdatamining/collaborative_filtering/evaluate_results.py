###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#
# A script that allows to evaluate the metrics for a given k-fold
###############################################################################

import sys
import math
import gzip
import pprint
import time
import measures # a file with our distances implementation
from sklearn.metrics import mean_squared_error
import scipy


class NestedDict(dict):
    """Subclass that inherit from dict. It allows to implement nested dicts."""
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


def parse_dataset(path):
    """A function that parse the dataset in the path defined as the argument.

    Args:
        path: a string that represents the path of the dataset to parse

    Return:
        The generator object, i.e. each call will run the loop and return the next value; thus, the generator is considered empty once the function runs but doesn't hit yield anymore.
    """
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


def nearest_neighbor(user, users_data, measure):
    """Finds a list of users that are nearest to a given user.

    Args:
        user: the reviewerID of the user that we want to recommend items to
        users_data: the complete datastore of ratings
        measure: the distance measure to use
            if 1:   Adjusted cosine similarity
            if 2:   Cosine similarity
            if 3:   Pearson correlation
            if 4:   Manhattan distance
            if 5:   Euclidean distance

    Return:
        A sorted list of users based on their distance to the input user
    """
    distances = []

    for u in users_data:
        if u != user:
            if measure == 1:
                distance = measures.adjusted_cosine_similarity(users_data[user], users_data[u])
            elif measure == 2:
                distance = measures.cosine_similarity(users_data[user], users_data[u])
            elif measure == 3:
                distance = measures.pearson_correlation(users_data[user], users_data[u])
            elif measure == 4:
                distance = measures.manhattan_distance(users_data[user], users_data[u])
            elif measure == 5:
                distance = measures.euclidean_distance(users_data[user], users_data[u])
            else:
                "ERROR! The similarity measure doesn't exist!"
            distances.append((u, distance))

    distances.sort(key=lambda itemTuple: itemTuple[1], reverse=True)

    return distances


def recommend(user, users_data, k, n, measure):
    """Gives a list of recommendations based on similar ratings.

    Args:
        user: the reviewerID of the user that we want to recommend items to
        users_data: the complete datastore of ratings
        k: the number of nearest neighbors to take into account
        n: the maximum number of recommendations to make
        measure: the distance measure to use
            if 1:   Adjusted cosine similarity
            if 2:   Cosine similarity
            if 3:   Pearson correlation
            if 4:   Manhattan distance
            if 5:   Euclidean distance

    Return:
        A sorted list of recommendations based on similar ratings of K-NN
    """
    total_distance = 0.0
    recommendations = {}
    ratings = {}
    counter_ratings = {}
    predicted_ratings = []
    expected_ratings = []

    nearest = nearest_neighbor(user, users_data, measure) # nearest user
    user_ratings = users_data[user] # (item, rating) given by the input user

    for i in range(k):
        total_distance += nearest[i][1] # sum of k-NN distances

    if total_distance != 0:
        for i in range(k): # accumulates all the k-NN ratings
            try:
                weight = nearest[i][1] / total_distance # neighbor's relative w.
            except ZeroDivisionError:
                print "ERROR! Cannot divide by zero."

            name = nearest[i][0] # name of the neighbor
            neighbor_ratings = users_data[name] # ratings for that neighbor

            # find (and store) items that user didn't rate
            for item in neighbor_ratings:
                if not item in user_ratings:
                    if item not in recommendations:
                        ratings[item] = neighbor_ratings[item]
                        counter_ratings[item] = 1
                        recommendations[item] = neighbor_ratings[item] * weight
                    else:
                        ratings[item] = ratings[item] + neighbor_ratings[item]
                        counter_ratings[item] += 1
                        recommendations[item] += neighbor_ratings[item] * weight

    for i in ratings:
        ratings[i] = ratings[i] / counter_ratings[i]

    for i in ratings:
        # print "Recommended: " + i
        if i in users_data_test[user]:
            # print "\tIt is also in the test set: " + i
            # print "\t\tPredicted vote: " + str(ratings[i])
            predicted_ratings.append(ratings[i])
            # print "\t\tExpected vote: " + str(users_data_test[user][i])
            expected_ratings.append(users_data_test[user][i])

    rms = 0

    if len(predicted_ratings) > 0:
        rms = math.sqrt(mean_squared_error(predicted_ratings, expected_ratings))
        print rms
    else:
        rms = -1
        print "There are no predicted objects in common."
    print "\n"

    recommendations = list(recommendations.items()) # make list from dict
    recommendations.sort(key=lambda itemTuple: itemTuple[1], reverse=True)

    #return recommendations[:n] # only get the first n items
    return rms

# Start the execution timer
start_time = time.time()

users_data = NestedDict() # create a new nested dictionary
users_data_test = NestedDict() # create a new nested dictionary


print "\nParsing training set..."

# Parse the dataset and populate the nested dictionary
for review in parse_dataset("../../data/k-fold/data_5/train_set_1234.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']
    users_data[user][product] = vote

print "Training set parsed.\n"


print "Parsing testing set..."

# Parse the dataset and populate the nested dictionary
for review in parse_dataset("../../data/k-fold/data_5/test_set_5.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']
    users_data_test[user][product] = vote

print "Testing set parsed.\n"

# Recommend a set of objects to a given user
print "\n"
print '*' * 80
print "Input data to compute:\n"
print "\tuser id\t\t%s" % user_id
print "\tk\t\t%d (nearest neighbors to take into account)" % k
print "\tn\t\t%s (maximum number of recommendations to make)" % n
print '*' * 80
print "\n"
print '*' * 80
print "List of recommendations in descending order:\n"


for i in range(20, 120, 20):
    k = i

    with open("../../data/k-fold/data_5/results_test_5.txt", "a") as f:
        f.write("K: " + str(k))
        f.write("\n=====\n")

    current_rms_adj = 0
    total_rms_adj = 0
    count_users_adj = 0

    current_rms_cos = 0
    total_rms_cos = 0
    count_users_cos = 0

    current_rms_pea = 0
    total_rms_pea = 0
    count_users_pea = 0

    current_rms_man = 0
    total_rms_man = 0
    count_users_man = 0

    current_rms_euc = 0
    total_rms_euc = 0
    count_users_euc = 0

    for u in users_data:
        if u in users_data_test:
            current_rms_adj = recommend(u, users_data, k, n, 1)
            current_rms_cos = recommend(u, users_data, k, n, 2)
            current_rms_pea = recommend(u, users_data, k, n, 3)
            current_rms_man = recommend(u, users_data, k, n, 4)
            current_rms_euc = recommend(u, users_data, k, n, 5)
            if current_rms_adj != -1:
                count_users_adj += 1
                total_rms_adj += current_rms_adj
            if current_rms_cos != -1:
                count_users_cos += 1
                total_rms_cos += current_rms_cos
            if current_rms_pea != -1:
                count_users_pea += 1
                total_rms_pea += current_rms_pea
            if current_rms_man != -1:
                count_users_man += 1
                total_rms_man += current_rms_man
            if current_rms_euc != -1:
                count_users_euc += 1
                total_rms_euc += current_rms_euc
    total_rms_adj = total_rms_adj / count_users_adj
    total_rms_cos = total_rms_cos / count_users_cos
    total_rms_pea = total_rms_pea / count_users_pea
    total_rms_man = total_rms_man / count_users_man
    total_rms_euc = total_rms_euc / count_users_euc

    with open("../../data/k-fold/data_5/results_test_5.txt", "a") as f:
        f.write("Adj cosine: ")
        f.write(str(total_rms_adj) + " on " + str(count_users_adj) + " recommendations.")
        f.write("\n")

        f.write("Cosine: ")
        f.write(str(total_rms_cos) + " on " + str(count_users_cos) + " recommendations.")
        f.write("\n")

        f.write("Pearson: ")
        f.write(str(total_rms_pea) + " on " + str(count_users_pea) + " recommendations.")
        f.write("\n")

        f.write("Manhattan: ")
        f.write(str(total_rms_man) + " on " + str(count_users_man) + " recommendations.")
        f.write("\n")

        f.write("Euclidean: ")
        f.write(str(total_rms_euc) + " on " + str(count_users_euc) + " recommendations.")
        f.write("\n")
        f.write("=====\n")

f.close()

# Print the execution time
print("--- Execution time: %s seconds ---" % (time.time() - start_time))
print "\n"
