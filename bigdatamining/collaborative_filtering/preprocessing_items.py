###############################################################################
# @authors          Alan Ramponi (151369), Davide Martintoni (171076)
# @courses          Data Mining / Big Data and Social Networks
# @description      A user-based collaborative filtering algorithm
#
# A preprocessing script to get only the items with N+ reviews
###############################################################################

import sys
import math
import gzip
import pprint
from collections import defaultdict


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


N = 20 # SET HERE THE MINIMUM NUMBER OF REVIEWS WE WANT FOR EACH ITEM

product_count = NestedDict() # create a new one for the product count

# Parse the dataset and populate the nested dictionary of product counters
for review in parse_dataset("../../data/k-fold/dataset_shuffled.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']

    # Update the count for every product that is in the original dataset
    if not product in product_count:
        product_count[product] = 1
    else:
        product_count[product] += 1

# Parse the dataset and populate the nested dictionary
for review in parse_dataset("../../data/k-fold/dataset_shuffled.json.gz"):
    user = review['reviewerID']
    product = review['asin']
    vote = review['overall']

    if product in product_count:
        if product_count[product] > N:
            with open("../../data/k-fold/dataset_preprocessed_1.txt","a") as f:
                f.write(str(review))
                f.write("\n")

f.close()
