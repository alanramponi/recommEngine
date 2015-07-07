###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#
# USAGE: python main.py [user id] [k] [n], where:
#   * user id: the (uppercase) alphanumeric user ID
#   * k: the number of nearest neighbors to take into account
#   * n: the maximum number of recommendations to make
###############################################################################

import sys
import math
import gzip
# import pprint
import time
import measures # a file with our distances implementation


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


def nearest_neighbor(user, users_data):
    """Finds a list of users that are nearest to a given user.

    Args:
        user: the reviewerID of the user that we want to recommend items to
        users_data: the complete datastore of ratings

    Return:
        A sorted list of users based on their distance to the input user
    """
    distances = []

    for u in users_data:
        if u != user:
            distance = measures.adjusted_cosine_similarity(users_data[user], users_data[u])
            distances.append((u, distance))

    distances.sort(key=lambda itemTuple: itemTuple[1], reverse=True)

    return distances


def recommend(user, users_data, k, n):
    """Gives a list of recommendations based on similar ratings.

    Args:
        user: the reviewerID of the user that we want to recommend items to
        users_data: the complete datastore of ratings
        k: the number of nearest neighbors to take into account
        n: the maximum number of recommendations to make

    Return:
        A sorted list of recommendations based on similar ratings of K-NN
    """
    total_distance = 0.0
    recommendations = {}

    nearest = nearest_neighbor(user, users_data) # nearest user (reviewerID)
    user_ratings = users_data[user] # (item, rating) given by the input user

    for i in range(k):
        total_distance += nearest[i][1] # sum of k-NN distances

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
                    recommendations[item] = neighbor_ratings[item] * weight
                else:
                    recommendations[item] += neighbor_ratings[item] * weight

    recommendations = list(recommendations.items()) # make list from dict
    recommendations.sort(key=lambda itemTuple: itemTuple[1], reverse=True)

    return recommendations[:n] # only get the first n items



# Start the execution timer
start_time = time.time()

# Check the input correctness
if len(sys.argv) != 4:
    print "\n"
    print '*' * 80
    print "Usage: python %s [user id] [k] [n]\n" % sys.argv[0]
    print "\tuser id\t\tthe (uppercase) alphanumeric user ID"
    print "\tk\t\tthe number of nearest neighbors to take into account"
    print "\tn\t\tthe maximum number of recommendations to make"
    print '*' * 80
    print "\n"
    sys.exit(1)

user_id = sys.argv[1] # the user ID
k = int(sys.argv[2]) # the number of nearest neighbors to take into account
n = int(sys.argv[3]) # the maximum number of recommendations to make

users_data = NestedDict() # create a new nested dictionary

# Parse the dataset and populate the nested dictionary
for review in parse_dataset("../../data/reviews_clothing_150k.json.gz"):
# for review in parse_dataset("../../data/reviews_grocery_50k.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']
    users_data[user][product] = vote

# FILE OUTPUT
# with open("../../tests/output_clothing.txt", "w") as f:
    # f.write(pprint.pformat(users_data))

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

recommendations = recommend(user_id, users_data, k, n) # testing for clothes
# print recommend("A2KBV88FL48CFS", users_data, 3, 10) # for static testing

# Print the results
print "\n".join(str(r) for r in recommendations)
print '*' * 80
print "\n"

# Print the execution time
print("--- Execution time: %s seconds ---" % (time.time() - start_time))
print "\n"
