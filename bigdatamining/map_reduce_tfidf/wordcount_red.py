#! /usr/bin/env python
import sys

# Reducer for the word count needed for the term frequency

# Example input (ordered by key)
# 1111111 word1
# 2222222 word1
# 2222222 word2
# 3333333 word1

# keys come grouped together
# so we need to keep track of state a little bit
# thus when the key changes (asin), we need to reset
# our counter, and write out the count we've accumulated


#init values
target_key = None
word_count = 0

for line in sys.stdin:
    
    line = line.strip()
    key, count = line.split("\t")
    count = int(count)


    # if this is the first iteration
    if not target_key:
        target_key = key
    
    # if they're the same, log it
    if key == target_key:
        word_count += 1
    else:
        # state change (previous line was k=x, this line is k=y)
        result = [target_key, word_count]
        print("\t".join(str(v) for v in result))
        target_key = key
        word_count = 1

# this is to catch the final counts after all records have been received.
print("\t".join(str(v) for v in [target_key, word_count]))


