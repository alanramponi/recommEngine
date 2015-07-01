import math
import parser

################################################################
#
#   Build a direct and an inverted index from the texts contained in a list
#
#   To test type: python indexing.py
#
################################################################

# Create the direct index
def get_index (reviews_list):

    index = []
    items = {}
    for i in range(len(reviews_list)):
        # Take terms from the text
        reviews_list[i]['terms'] = parser.extract_terms(reviews_list[i]['text'])
        # Now text is not needed anymore
        del reviews_list[i]['text']
        #check if reviews has its own asin
        if not reviews_list[i]['asin']:
            print "Oops!  I miss my ASIN"
            return
        # The document ID is its position within the direct index
        reviews_list[i]['id'] = len(index)
        index.append(reviews_list[i])
        items[reviews_list[i]['id']] = reviews_list[i]['asin']
    return index, items

# Return all terms with number of occurrences
def terms_with_count (terms):
	count = {}
	for term in terms:
		if term in count:
			count[term] += 1
		else:
			count[term] = 1
	return count

# Invert the direct index
def invert_index (direct_index):

	# inverted index of the text.
	# The index maps each term to a list of triplets
	# (asin, occurrences, term_frequency)
	inverted_index = {}

	for reviews in direct_index:

		itemid = reviews['id']
		terms = reviews['terms']

		count = terms_with_count (terms)

		# Add the temporary count to the global inverted index
		for t, c in count.items():
			tf = float(c)/len(terms)
			if t in inverted_index:
				inverted_index[t]['occurrences'].append ((itemid, c, tf))
			else:
				inverted_index[t] = {
					# The term ID is its position within the inverted index
					'termid': len(inverted_index),
					'occurrences': [(itemid, c, tf)]
				}

	# Now add the IDF of each term in its corresponding inverted index entry
	n_reviews = float(len(direct_index))
	for t, l in inverted_index.items():
		# Compute the term's IDF
		idf = math.log (n_reviews / len(l['occurrences']))
		if idf > 0:
			l['idf'] = idf
		else:
			# If IDF == 0, remove term from inverted index
			del inverted_index[t]

	return inverted_index

# Given an inverted index, compute the IDF threshold value such that a given fraction
# of terms is above that level
def IDF_threshold (inverted_index, term_fraction = .99):
	# Sort all IDFs by ascending value
	idf_list = sorted([l['idf'] for l in inverted_index.values()])
	# Find the appropriate position in the list
	threshold_index = int(len(idf_list)*(1-term_fraction))
	# Return the value in the sorted list
	return idf_list[threshold_index]


if __name__ == '__main__':
    #prepare a list of documents with the test dataset
    list = parser.extract_reviews("test_reviews.json.gz")
    direct_index = get_index(list)
    print 'Gotcha direct index: ' + str(direct_index)
    print 'Now computing the inverted index...'
    inverted_index = invert_index(direct_index)
    print len(inverted_index), 'terms indexed.'
    print '99% IDF threshold is', IDF_threshold(inverted_index, .99)
