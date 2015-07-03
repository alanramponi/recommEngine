#! /usr/bin/env python
import sys
import operator

#init values
target_key = None
word_count = 0
temp_counter = {}

for line in sys.stdin:
    
    	line = line.strip()
    	asin, value = line.split("\t")

	word, count = value.split("=")
	
	count = int(count)	

    	# if this is the first iteration
    	if not target_key:
        	target_key = asin
    
    	# if they're the same, log it
    	if asin == target_key:
		temp_counter[word] = count
        	word_count += count
    	else:
        	# state change (previous line was k=x, this line is k=y)
		for k,v in temp_counter.iteritems():
			new_key = str(k) + "@" + asin 
			new_value = str(float(v)/word_count)
			result = [new_key, new_value]
        		print("\t".join(str(v) for v in result))		
		
		# reset for next stage
		word_count = 0
		temp_counter = {}
		temp_counter[word] = count
        	target_key = asin
		word_count += count

# this is to catch the final counts after all records have been received.
for k,v in temp_counter.iteritems():
	new_key = str(k) + "@" + asin
	new_value = str(float(v)/word_count)
	result = [new_key, new_value]
	print("\t".join(str(v) for v in result))

