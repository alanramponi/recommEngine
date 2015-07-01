import sys
import time

import parser
import indexing
import TFIDF
import jaccard

#############################################################
#
#   All togeter NOW!!!!
#
#   Example:
#   python main.py .95  #(if you want to type the ASIN of the item for you want suggestion)
#   python main.py .95 "i'm a possible text that you want to use a searched text"  #(to type your text)
#
#############################################################

#SELECT HERE DATASET
path = "../../data/1000_reviews.json.gz"

#get IDF thrashold if one
term_fraction = None if len(sys.argv) < 2 else float(sys.argv[1])
#get search text if one
search_text = None if len(sys.argv) < 3 else sys.argv[2]

print "Take the list of reviews"
start = time.time()
reviews = parser.extract_reviews(path)
direct_index, items = indexing.get_index(reviews)
print len(direct_index), ' review\'s direct index.'
print 'Now computing the inverted index'
inverted_index = indexing.invert_index (direct_index)
print len(inverted_index), 'terms indexed.'

# For convenience, remember the number of terms and reviews
n_reviews = len(direct_index)
n_terms = max(t['termid'] for t in inverted_index.values()) + 1

# Compute the optional IDF threshold
idf_threshold = None if not term_fraction else indexing.IDF_threshold (inverted_index, term_fraction)
if idf_threshold:
    print "IDF threshold set at", idf_threshold

##############################################################

print 'Computing TFIDF representations'
TFIDFs = TFIDF.compute_all_TFIDFs (inverted_index, idf_threshold)

#print "TFIDF  " + str(TFIDFs)

#####################################################################
target_index = None

if search_text:
    # Given a search_text, compute its TFIDF representation
    print 'Computing search text\'s TFIDF representation'
    search_terms = parser.extract_terms(search_text)
    searched_TFIDF = TFIDF.compute_new_TFIDF (search_terms, inverted_index, idf_threshold)

    # Warn if the search_text is empty due to a high IDF threshold
    if len(searched_TFIDF) == 0:
        print '*** WARNING *** Empty search, IDf threshold too high'

else:
    #ask for the target item:
    asin = raw_input("Please enter an item ASIN (e.g. 1603112251): ")
    
    print 'Find TFIDF representation'
    target_index = next((id for id, code in items.items() if code == asin), None)
    
    # Error if the targeted ASIN is not found
    if target_index == None:
        sys.exit('*** FATAL *** item not found')
    else:
        searched_TFIDF = TFIDFs[target_index]
        search_terms = direct_index[target_index]['terms']

######################################################################

## cosine similarities between reviews
cosine_similarities = [[TFIDF.cosine_similarity(d1,d2) for d2 in TFIDFs] for d1 in TFIDFs]

sets = jaccard.compute_all_sets (inverted_index, idf_threshold)


jacard_similarities = [[jaccard.jaccard_coefficient(d1,d2) for d2 in sets] for d1 in sets]

## Compute the set representation
print 'Computing searched set representation'
searched_set = jaccard.compute_new_set (search_terms, inverted_index, idf_threshold)


print 'Computing document ranking based on Euclidean, Cosine and Jaccard'
euclidean_ranking = []
cosine_ranking = []
jaccard_ranking = []
for i in range(n_reviews):
    if target_index != None and i != target_index:
        euclidean_ranking.append( (i, TFIDF.Euclidean_distance (searched_TFIDF, TFIDFs[i])) )
        cosine_ranking.append( (i, TFIDF.cosine_similarity (searched_TFIDF, TFIDFs[i])) )
        jaccard_ranking.append( (i, jaccard.jaccard_coefficient (searched_set, sets[i])) )

euclidean_ranking.sort (key = lambda t: t[1])
cosine_ranking.sort (key = lambda t: t[1], reverse = True)
jaccard_ranking.sort (key = lambda t: t[1], reverse = True)

######################################################################

#print results for desired item

end = time.time()
print "in " + str(end - start) + " seconds"

print 'Resulting top rankings:\nEuclidean distance\t\tCosine similarity\t\tJaccard similarity'
for i in range(10):
    print '%s\t%f\t%s\t%f\t%s\t%f' % (
                                      items[euclidean_ranking[i][0]],
                                      euclidean_ranking[i][1],
                                      items[cosine_ranking[i][0]],
                                      cosine_ranking[i][1],
                                      items[jaccard_ranking[i][0]],
                                      jaccard_ranking[i][1])