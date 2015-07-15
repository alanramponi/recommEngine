###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#                   : a file with our distances implementation
###############################################################################

import math
import numpy


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

    if n != 0:
        denominator = math.sqrt(summation_power_x - (pow(summation_x, 2) / n)) * math.sqrt(summation_power_y - (pow(summation_y, 2) / n))
    else:
        return 0

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

    denominator = math.sqrt(summation_power_x) * math.sqrt(summation_power_y)

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

    mean_x = numpy.mean(ratings_1.values()) # mean value of ratings vector x
    mean_y = numpy.mean(ratings_2.values()) # mean value of ratings vector y

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

    denominator = math.sqrt(summation_power_x) * math.sqrt(summation_power_y)

    if (denominator == 0):
        return 0
    else:
        numerator = summation_xy
        return numerator / denominator


if __name__ == '__main__':
    print "\n"
    print '*' * 80
    print "Please execute: python main.py [user id] [k] [n]\n"
    print "\tuser id\t\tthe (uppercase) alphanumeric user ID"
    print "\tk\t\tthe number of nearest neighbors to take into account"
    print "\tn\t\tthe maximum number of recommendations to make"
    print '*' * 80
    print "\n"
