#! /usr/bin/env python

import sys


for line in sys.stdin:
	#read line and parse with json
	line = line.strip()
	key, tf = line.split("\t")
	word, asin = key.split("@")
	new_value = asin + "=" + tf
   	print("\t".join(str(v) for v in [word, new_value]))
