import pandas as pd
from os import path
import re

risk_factors = ["ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk"]

def generate_ngrams(s, n):
    s = s.lower()
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', s)
    tokens = [token for token in s.split(" ") if token != ""]
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

for rf in risk_factors:

    file_vocabulary = open("vocabularys/vocabulary_"+ rf +"_stemmed.txt","r")

    vocabulary_str = file_vocabulary.read()

    vocabulary = vocabulary_str.split()

    word_bag = list(set(vocabulary))

    output = open("vocabularys/wordbag_"+rf+".txt", "w")

    for w in word_bag:
        output.write(w + " ")

    output.close()

    from collections import Counter
    c = Counter(vocabulary)

    top = c.most_common(100)

    output = open("vocabularys/wordbag_"+rf+"_top_100.txt", "w")

    for w in top:
        output.write(w[0] + " ")

    output.close()

    top = c.most_common(100)

    output = open("vocabularys/wordbag_"+rf+"_top_50.txt", "w")

    for w in top:
        output.write(w[0] + " ")

    
    output.close()

    bigrams = generate_ngrams(vocabulary_str, 2)

    c = Counter(bigrams)

    top = c.most_common(100)

    output = open("vocabularys/wordbag_bigrams_"+rf+"_top_50.txt", "w")

    for w in top:
        output.write(w[0] + "\;")

    output.close()
    
    trigrams = generate_ngrams(vocabulary_str, 3)

    c = Counter(trigrams)

    top = c.most_common(50)

    output = open("vocabularys/wordbag_trigrams_"+rf+"_top_50.txt", "w")

    for w in top:
        output.write(w[0] + "\;")

    output.close()

    c = Counter(bigrams)

    top = c.most_common(100)

    output = open("vocabularys/wordbag_bigrams_"+rf+"_top_100.txt", "w")

    for w in top:
        output.write(w[0] + "\;")

    output.close()

    print(len(word_bag))
