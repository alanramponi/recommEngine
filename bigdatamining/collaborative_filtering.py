###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (17xxxx)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
###############################################################################

from math import sqrt
import numpy
import gzip
import pprint


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


def manhattan_distance(ratings_1, ratings_2):
    """Computes the Manhattan distance between two users' dictionaries.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings

    Return:
        A call to minkowski_distance with order equal to 1
    """
    return minkowski_distance(ratings_1, ratings_2, 1)


def euclidean_distance(ratings_1, ratings_2):
    """Computes the Euclidean distance between two users' dictionaries.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings

    Return:
        A call to minkowski_distance with order equal to 2
    """
    return minkowski_distance(ratings_1, ratings_2, 2)


def minkowski_distance(ratings_1, ratings_2, order):
    """Generalization algorithm of both the Manhattan and Euclidean distance.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings
        order: the order that represents a particular distance metric
            if 1:   Manhattan distance
            if 2:   Euclidean distance
            if INF: Chebyshev distance (not implemented)

    Return:
        A real number that represents the distance between the two dictionaries
    """
    distance = 0
    common_ratings = False

    for key in ratings_1:
        if key in ratings_2:
            distance += pow(abs(ratings_1[key]-ratings_2[key]), order)
            common_ratings = True

    if common_ratings:
        return pow(distance, 1.0/order)
    else:
        return 0 # so there are no ratings in common


def pearson_correlation(ratings_1, ratings_2):
    """Computes the Pearson correlation between two sets of users' ratings.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings

    Return:
        A number that represents the distance between the two dictionaries
            In the output range [-1,1].
    """
    n = 0
    summation_x = summation_y = summation_xy = 0
    summation_power_x = summation_power_y = 0

    for key in ratings_1:
        if key in ratings_2: # only if both x and y have rated the item
            n += 1
            x = ratings_1[key] # rating by x for a particular item
            y = ratings_2[key] # rating by y for a particular item
            summation_x += x # the sum of Xi, from i to n
            summation_y += y # the sum of Yi, from i to n
            summation_xy += x*y # the sum of the product Xi*Yi, from i to n
            summation_power_x += pow(x, 2) # the sum of Xi^2, from i to n
            summation_power_y += pow(y, 2) # the sum of Yi^2, from i to n
    denominator = sqrt(summation_power_x - (pow(summation_x, 2) / n)) * sqrt(summation_power_y - (pow(summation_y, 2) / n))

    if (denominator == 0):
        return 0
    else:
        numerator = summation_xy - ((summation_x * summation_y) / n)
        return numerator / denominator


def cosine_similarity(ratings_1, ratings_2):
    """Computes the Cosine similarity between two sets of users' ratings.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings

    Return:
        A real number that represents the distance between the two dictionaries
            In the output range [-1,1].
    """
    intersection_size = 0
    summation_xy = summation_power_x = summation_power_y = 0

    for key in ratings_1:
        x = ratings_1[key] # rating by x for a particular item
        if key in ratings_2:
            y = ratings_2[key] # rating by y for a particular item
            intersection_size += 1
        else:
            y = 0
        summation_xy += x*y # the sum of the product Xi*Yi, from i to n
        summation_power_x += pow(x, 2) # the sum of Xi^2, from i to n
        summation_power_y += pow(y, 2) # the sum of Yi^2, from i to n

    if (len(ratings_2) > intersection_size):
        for key in ratings_2:
            y = ratings_2[key]
            if key not in ratings_1:
                x = 0
                summation_xy += x*y
                summation_power_x += pow(x, 2)
                summation_power_y += pow(y, 2)

    denominator = sqrt(summation_power_x) * sqrt(summation_power_y)

    if (denominator == 0):
        return 0
    else:
        numerator = summation_xy
        return numerator / denominator


def adjusted_cosine_similarity(ratings_1, ratings_2):
    """Computes the Adjusted cosine similarity between two sets of users' ratings. Thus, the difference in rating scale between different users are taken into account.

    Args:
        ratings_1: the first dictionary of ratings
        ratings_2: the second dictionary of ratings

    Return:
        A real number that represents the distance between the two dictionaries
            In the output range [-1,1].
    """
    intersection_size = 0
    summation_xy = summation_power_x = summation_power_y = 0

    mean_x = numpy.mean(ratings_1.values())
    mean_y = numpy.mean(ratings_2.values())

    for key in ratings_1:
        x = ratings_1[key] # rating by x for a particular item
        if key in ratings_2:
            y = ratings_2[key] # rating by y for a particular item
            intersection_size += 1
            summation_xy += (x-mean_x)*(y-mean_y)
            summation_power_x += pow(x-mean_x, 2)
            summation_power_y += pow(y-mean_y, 2)
        else:
            y = 0
            summation_xy += (x-mean_x)*(y)
            summation_power_x += pow(x-mean_x, 2)
            summation_power_y += pow(y, 2)

    if (len(ratings_2) > intersection_size):
        for key in ratings_2:
            y = ratings_2[key] # rating by y for a particular item
            if key not in ratings_1:
                x = 0
                summation_xy += (x)*(y-mean_y)
                summation_power_x += pow(x, 2)
                summation_power_y += pow(y-mean_y, 2)

    denominator = sqrt(summation_power_x) * sqrt(summation_power_y)

    if (denominator == 0):
        return 0
    else:
        numerator = summation_xy
        return numerator / denominator


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
            distance = adjusted_cosine_similarity(users_data[user], users_data[u])
            distances.append((u, distance))

    distances.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
    # print distances[:10]

    return distances


def recommend(user, users_data):
    """Gives a list of recommendations based on similar ratings.

    Args:
        user: the reviewerID of the user that we want to recommend items to
        users_data: the complete datastore of ratings

    Return:
        A sorted list of recommendations based on similar ratings of K-NN
    """
    k = 3
    # n = 5 # the maximum number of recommendations to make
    total_distance = 0.0
    recommendations = {}

    # the ID of the nearest user
    nearest = nearest_neighbor(user, users_data) # A0004478EF5NFPHLGCWG

    # a list of (item, rating) pairs given by the input user
    user_ratings = users_data[user] # {'B0001BGTSA': 5.0, 'B0001BGTV2': 5.0}

    for i in range(k):
        total_distance += nearest[i][1]
        # print total_distance

    # Iterate through the k nearest neighbors accumulating their ratings
    for i in range(k):
        # compute slice of pie
        weight = nearest[i][1] / total_distance # TODO(Alan): divisione per 0
        name = nearest[i][0] # name of the user
        neighbor_ratings = users_data[name] # ratings for this user

        # Find items neighbor rated that user didn't
        for item in neighbor_ratings:
            if not item in user_ratings:
                if item not in recommendations:
                    recommendations[item] = neighbor_ratings[item] * \
                                        weight
                else:
                    recommendations[item] = recommendations[item] + \
                                        neighbor_ratings[item] * \
                                        weight

    # Make list from dictionary (TODO(Alan): and only get the first n items)
    recommendations = list(recommendations.items())
    # recommendations = list(recommendations.items())[n]

    recommendations.sort(key=lambda itemTuple: itemTuple[1], reverse=True)
    return recommendations



users_data = NestedDict() # create a new nested dictionary

# Parse the dataset and populate the nested dictionary
#for review in parse_dataset("../RESOURCES/BIG-DATA_Datasets/reviews_Grocery_and_Gourmet_Food.json.gz"):

for review in parse_dataset("../data/reviews_clothing_150k.json.gz"):
    # for review in parse_dataset("../data/reviews_grocery_50k.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']
    users_data[user][product] = vote

# CONSOLE OUTPUT
# pprint.pprint(users_data)

# FILE OUTPUT
# with open("../tests/output_clothing.txt", "w") as f:
    # f.write(pprint.pformat(users_data))

# Recommend a set of object to a given user
print recommend("A2KBV88FL48CFS", users_data) # testing for clothes
# print recommend("A3D6OI36USYOU1", users_data) # testing for grocery
