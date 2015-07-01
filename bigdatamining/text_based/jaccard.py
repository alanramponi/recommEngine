# Given a complete inverted index and an optional IDF threshold(indexing.py),
# compute and return the list of set representations of all indexed texts.
def compute_all_sets (inverted_index, idf_threshold = None):
	sets = []
	for l in inverted_index.values():
		if not idf_threshold or l['idf'] >= idf_threshold:
			termid = l['termid']
			for o in l['occurrences']:
				docid = o[0]
				while len(sets) < docid + 1:
					sets.append (set())
				sets[docid].add (termid)
	return sets

# Given the term list of an unindexed text, an inverted index, and an optional IDF threshold,
# compute and return the set representation of the text.
def compute_new_set (new_document_terms, inverted_index, idf_threshold = None):
	return set (
		inverted_index[term]['termid']
			for term in new_document_terms 
			if term in inverted_index
				and (not idf_threshold or inverted_index[term]['idf'] >= idf_threshold)
	)

# Compute the Jaccard coefficient between two sets
def jaccard_coefficient (d1, d2):
	intersection_size = len (d1 & d2)
	return float(intersection_size) / (len(d1) + len(d2) - intersection_size)
