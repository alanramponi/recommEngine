#! /usr/bin/env python
import sys
import operator
import os


#init values
target_key = None
item_count = 0
temp_counter = {}

for line in sys.stdin:
    
	tot_item = int(os.environ["TOT_LINE"])

    line = line.strip()
    word, value = line.split("\t")

	asin, tf = value.split("=")	

    # if this is the first iteration
    if not target_key:
        target_key = word
    
    # if they're the same, log it
    if word == target_key:
        temp_counter[asin] = tf
        item_count += 1
    else:
        # state change (previous line was k=x, this line is k=y)
		for k,v in temp_counter.iteritems():
			new_key = target_key + "@" + k
			tfidf = float(v) * log((float(tot_item)/item_count), 10)
			result = [new_key, tfidf]
            print("\t".join(str(v) for v in result))
		
		# reset for next stage
		item_count = 1
		temp_counter = {}
		temp_counter[asin] = word
        target_key = word

# this is to catch the final counts after all records have been received.
for k,v in temp_counter.iteritems():
	new_key = str(v) + "@" + k 
	tfidf = float(tf) * (float(item_count)/tot_item)
	result = [new_key, tfidf]
    print("\t".join(str(v) for v in result))

