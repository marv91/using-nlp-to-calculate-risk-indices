
# coding: utf-8

# In[1]:


import sqlite3
import numpy as np
import pandas as pd
from nltk.corpus import stopwords

from nltk.stem.snowball import SnowballStemmer

conn = sqlite3.connect('data.db')
c = conn.cursor()
c.execute("select * from data_stemmed")
result = c.fetchall()

dates_ = []

for r in result:
    dates_.append(r[0])
    
dates_ = np.array(dates_,dtype=np.datetime64)

articles_ = []

for r in result:
    articles_ += [r[1]]

length_ = []

for k in range(0,len(articles_)):
    length_ += [len(articles_[k])]
    


import matplotlib.pyplot as plt
plt.title("article length")
plt.plot(dates_, length_, color = "black")
plt.ylim(0, 140000) 
plt.show()

plt.boxplot(length_)
plt.xticks([1], [''])
plt.title("article length box plot")
plt.xlabel("article length")
plt.show()

cut_1 = pd.Series(length_).quantile(0.975)
cut_2 = pd.Series(length_).quantile(0.025)

print(cut_1)
print(cut_2)

articles = []
dates = []

counter_k = 0

for k in range(0,len(articles_)):
    if(len(articles_[k]) > cut_2 and len(articles_[k]) < cut_1):
        articles.append(articles_[k])
        dates.append(dates_[k])
        
length_ = []

for k in range(0,len(articles)):
    length_ += [len(articles[k])]

import matplotlib.pyplot as plt
plt.title("article length after outlier removal")
plt.plot(dates, length_, color = "black")
plt.ylim(0, 140000) 
plt.show()

plt.boxplot(length_)
plt.xticks([1], [''])
plt.title("box plot after outlier removal")
plt.xlabel("article length")
plt.show()

dates = np.array(dates,dtype=np.datetime64)

print(len(articles_))
print(len(articles))


# In[4]:


def cosine_sim(X,Y):
    x = np.array(X)
    y = np.array(Y)

    return np.dot(x,y) / (np.linalg.norm(x)*np.linalg.norm(y))


risk_factors = ["manually", "ClimateChange_Risk", "International_Risk", "Economic_Risk", "Technology_Risk"]
#risk_factors = ["Economic_Risk"]

tf_matrix = []
mapping = []
tf_vocs = []

for rf in risk_factors:
    
    print("starting calculation: " + rf)
    
    if rf is not "manually":

        wb_bi = open("vocabularys/wordbag_bigrams_"+rf+"_top_50.txt")

        wb_bi = wb_bi.read()
        wb_bi = wb_bi.split("\;")

        wb_uni = open("vocabularys/wordbag_"+rf+"_top_50.txt")

        wb_uni = wb_uni.read()
        wb_uni = wb_uni.split()

        wb = wb_uni + wb_bi
        
        wb = list(dict.fromkeys(wb))
        
        voc_file = open("vocabularys/vocabulary_"+rf+"_stemmed.txt")
        voc = voc_file.read()
        
    else:
        
        wb = open("vocabularys/wordbag_manually_stemmed.txt").read().split("\;")
        voc_file = open("vocabularys/vocabulary_manually_stemmed.txt")
        voc = voc_file.read()
        
    result = []

    sw = set(stopwords.words('english'))
    sw.update(["addit", "htm", "von","all","rights","reserved","copyright","section","length","headline","abstract","language"
                               "byline","load","date","loaddate","graphic","document","type","documenttype","publication","publicationtype","newspaper","editorial","letters",
                               "english","new","york","times","wall","street","journal","abstracts","information","bank","wsj","company","combination","photograph",
                                "graphic","code","diagram","charts","graphs","page","column","pg","words","january","february","march","april","may","june","july", "may", "et", "al", 
                                "august","september","october","november","december","general","cartoon","monday","tuesday","wednesday","thursday","friday","saturday","sunday"
                               "graph","photo","language","byline","head","tabl","sourc","year","figur"])


    corpus = []
    tfidf_articles = []

    from sklearn.feature_extraction.text import TfidfVectorizer

    vectorizer = TfidfVectorizer(stop_words = sw, ngram_range = (1,2), vocabulary = wb) 

    tfidf_articles = vectorizer.fit_transform(articles).toarray()

    mapping += [vectorizer.vocabulary_]
    
    voc_doc = [voc]

    tfidf_voc = vectorizer.transform(voc_doc).toarray()
    
    tf_vocs += [tfidf_voc[0]]
    
    tf_matrix += [tfidf_articles]

    ts = []
    for i in range(len(tfidf_articles)):
        ts.append(cosine_sim(tfidf_articles[i],tfidf_voc[0]))
        
    ts_new = pd.Series(np.power(np.array(ts),1), index=dates)
    ts_new.to_csv(rf+"_index_raw.csv")
    
    print("finished calculation: " + rf)

