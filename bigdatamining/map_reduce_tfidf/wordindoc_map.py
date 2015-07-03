#! /usr/bin/env python

import sys


for line in sys.stdin:
	#read line and parse with json
	line = line.strip()
	key, count = line.split("\t")
	word, asin = key.split("@")
	new_value = word + "=" + count
   	print("\t".join(str(v) for v in [asin, new_value]))
