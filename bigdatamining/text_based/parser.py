import nltk
import sys
import gzip
import json

######################################################
#
#   Parser that take a text and reduce it to a tokenized/stemmed
#   string.
#
#   To debug call python parser.py
#
######################################################


def extract_terms(text):
    #divide text in tokens and labeld them based on what type of word they are
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)
    
    #filter the list and select only nouns
    filtered = []
    for tupla in tagged:
        if 'NN' in tupla[1]:
            filtered.append(tupla[0])

    #stemm the list and join it in a string
    stemmer = nltk.SnowballStemmer("english")
    lst = []
    for i in range(len(filtered)):
                lst.append(stemmer.stem(filtered[i]))
    return ' '.join(lst)

def extract_reviews(path):
    set = gzip.open(path, 'r')
    
    list = []
    already_parsed = {}
    
    for line in set:
        
        temp = {}
        
        parsedline = json.loads(line)
        try:
            
            if 'asin' in parsedline and 'reviewText' in parsedline: #ASIN not exists skip
                temp['asin'] = parsedline['asin']
                temp['text'] = parsedline['reviewText']
                #if this item has already a review concat this with the otherone
                if temp['asin'] in already_parsed:
                    index = next(i for (i, d) in enumerate(list) if d["asin"] == temp['asin'])
                    list[index]['text'] = list[index]['text'] + " " + temp['text']
                else:
                    already_parsed[temp['asin']] = True
                    list.append(temp)
    
    
        except (RuntimeError, TypeError, NameError):
            print "EXCEPTION: error " + str(RuntimeError)

    #print "Found " + str(len(list))
    return list



if __name__ == '__main__':
    test_string = raw_input("Please enter something: ")
    result = extract_terms (test_string)
    print result