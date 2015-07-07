#! /usr/bin/env python

import sys


for line in sys.stdin:
    line = line.strip()
    key, tfidf = line.split("\t")
    word, asin = key.split("@")
    new_key = asin + "@" + word
    print("\t".join(str(v) for v in [new_key, tfidf]))