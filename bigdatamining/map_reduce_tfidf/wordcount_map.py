#! /usr/bin/env python

import sys
import json
import re

for line in sys.stdin:
	line = line.strip()

    	try:
    		parsedline = json.loads(line)
    	except ValueError, e:
        	continue
	if 'asin' in parsedline and 'reviewText' in parsedline:
		asin = parsedline['asin']
		text = parsedline['reviewText']
    	else:
		sys.exit('Fatal asin not found')
   
	text = text.lower()

	token = re.sub("[^\w]", " ",  text).split()

	
	stopWords = ['a','able','about','across','after','all','almost','also','am','among',\
             'an','and','any','are','as','at','be','because','been','but','by','can',\
             'cannot','could','dear','did','do','does','either','else','ever','every',\
             'for','from','get','got','had','has','have','he','her','hers','him','his',\
             'how','however','i','if','in','into','is','it','its','just','least','let',\
             'like','likely','may','me','might','most','must','my','neither','no','nor',\
           'not','of','off','often','on','only','or','other','our','own','rather','said',\
             'say','says','she','should','since','so','some','than','that','the','their',\
             'them','then','there','these','they','this','tis','to','too','twas','us',\
             'wants','was','we','were','what','when','where','which','while','who',\
             'whom','why','will','with','would','yet','you','your']
	stemEndings = ( "s", "es", "ed", "er", "ly" )
	punctuation = [ ".", ",", ":", ";", "!", "?" ]	

	filtered = []

	for w in token:
		if not w in stopWords and not w in punctuation:
			if w.endswith(stemEndings):
				w = w[:len(w)-2]
			elif w.endswith("ing"):
				w = w[:len(w)-3]
			if len(w) > 2:
				filtered.append(w)

	for i in range(len(filtered)):
    		word = filtered[i]
        	#now emit partial <k, v>
        	word = word + "@" + asin
        	result = [word, "1"]
        	print("\t".join(result))
