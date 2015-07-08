#! /usr/bin/env python
import sys
import operator

#init values
target_key = None
item_count = 0
new_value = []

for line in sys.stdin:
    
    line = line.strip()
    key, tfidf = line.split("\t")
        
    asin, word = key.split("@")
        
    # if this is the first iteration
    if not target_key:
        target_key = asin
    
    # if they're the same, log it
    if asin == target_key:
        v = word + "=" + tfidf
        new_value.append(v)
    else:
        result_value = "@".join(str(v) for v in new_value)
        result = [asin, result_value]
        print("\t".join(str(v) for v in result))
        # reset for next stage
        target_key = asin
        new_value = []
        v = word + "=" + tfidf
        new_value.append(v)

# this is to catch the final counts after all records have been received.
result_value = "@".join(str(v) for v in new_value)
result = [asin, result_value]
print("\t".join(str(v) for v in result))