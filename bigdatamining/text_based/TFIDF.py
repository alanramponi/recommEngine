#! /usr/bin/python
#
# Given a direct and inverted index, compute the corresponding TFIDF representation.

import math

import indexing

# Given a complete inverted index and an optional IDF threshold,
# compute and return the list of TFIDF representations of all indexed documents.
# Each TFIDF representation is stored as a list of (index, value) pairs sorted by index.
def compute_all_TFIDFs (inverted_index, idf_threshold = None):
	# Start with an empty list
    TFIDFs = []
	# Scan all terms
    #print "n_terms: " + str(len(inverted_index))
    for l in inverted_index.values():
        idf = l['idf']
		# Skip the term if it's below the optional threshold
        if idf_threshold and idf < idf_threshold:
			continue
        termid = l['termid']
        #print "L: " + str(l)
		# Add the term to all TFIDF vectors of documents it occurs in
        for d, c, tf in l['occurrences']:
            #print "D: " + str(d) + " C:" + str(c) + " tf:" + str(tf)
            while len(TFIDFs) < d+1:
				TFIDFs.append([])
            TFIDFs[d].append ((termid, tf*idf))
            #print "TermID: " + str(termid) + " rating"  + str(tf*idf)
	# Sort all representations by index
    for v in TFIDFs:
		v.sort()
    return TFIDFs

# Given the term list of an unindexed document (e.g., a query), an inverted index, and an optional IDF threshold,
# compute and return the TFIDF representation of the document.
def compute_new_TFIDF (new_document_terms, inverted_index, idf_threshold = None):
	# Comput the multiplicity of each term
	counts = indexing.terms_with_count (new_document_terms)
	TFIDF = []
	# Normalization scale for TF
	scale = 1.0 / len(new_document_terms)
	# For all terms with their multiplicity,
	for t, c in counts.items():
		try:
			entry = inverted_index[t]
			idf = entry['idf']
			# if appropriate, add the TFIDF entry for the term.
			if not idf_threshold or idf >= idf_threshold:
				TFIDF.append ((entry['termid'], c * scale * idf))
		except:
			pass
	# Sort by term id and return
	return sorted (TFIDF)

# Compute the Euclidean distance between two (unnormalized) TFIDF representations
def Euclidean_distance (d1, d2):
    print "D1: " + str(d1)
    print "D2: " + str(d2)
    s = 0.0
    i1 = 0
    i2 = 0
    while i1 < len(d1) or i2 < len(d2):
		if i1 == len(d1):
			v = d2[i2][1]
			i2 += 1
		elif i2 == len(d2):
			v = d1[i1][1]
			i1 += 1
		elif d1[i1][0] < d2[i2][0]:
			v = d1[i1][1]
			i1 += 1

		elif d2[i2][0] < d1[i1][0]:
			v = d2[i2][1]
			i2 += 1
		else:
			v = d1[i1][1] - d2[i2][1]
			i1 += 1
			i2 += 1
		s += v * v
    return math.sqrt (s)

# Compute the cosine similarity (normalized dot product) between two TFIDF representations
def cosine_similarity (d1, d2):
	s = 0.0
	s1 = 0.0
	s2 = 0.0
	i1 = 0
	i2 = 0
	while i1 < len(d1) or i2 < len(d2):
		if i1 == len(d1):
			s2 += d2[i2][1] * d2[i2][1]
			i2 += 1
		elif i2 == len(d2):
			s1 += d1[i1][1] * d1[i1][1]
			i1 += 1
		elif d1[i1][0] < d2[i2][0]:
			s1 += d1[i1][1] * d1[i1][1]
			i1 += 1
		elif d2[i2][0] < d1[i1][0]:
			s2 += d2[i2][1] * d2[i2][1]
			i2 += 1
		else:
			s += d1[i1][1] * d2[i2][1]
			s1 += d1[i1][1] * d1[i1][1]
			s2 += d2[i2][1] * d2[i2][1]
			i1 += 1
			i2 += 1
	return s / (math.sqrt(s1 * s2)) if s1 and s2 else 0.0
