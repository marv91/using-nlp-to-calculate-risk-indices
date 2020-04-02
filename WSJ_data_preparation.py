import datetime 
import os

import sqlite3

# set directory path with WSJ articles
directory = "WSJ Abstracts"
conn = sqlite3.connect('data.db')

c = conn.cursor()

c.execute('''CREATE TABLE articles (date date, body text)''')

def month_string_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


N = len(os.listdir(directory))
co = 0
for filename in os.listdir(directory):

    co += 1

    print(co/N)

    if filename.endswith(".TXT"): 
        file = open(directory + "/" + filename)

        file_text = file.read()

        articles = file_text.split("Dokument")

        for article in articles:
   
            try:

                date_raw = article.splitlines(True)[6]

                date = date_raw.replace(",","")
                date_parts = date.split()

                month = month_string_to_number(date_parts[0])
                day = int(date_parts[1])
                year = int(date_parts[2])

                if "ABSTRACT" in article.split("LENGTH")[1]:

                    temp = article.split("LENGTH")[1].split("ABSTRACT")
                    temp_ = temp[1].splitlines()
                
                    temp_c = 2

                    abstract = ""

                    while(not temp_[temp_c] == ''):
                        abstract = abstract + temp_[temp_c]
                        temp_c += 1
                                          
                   
                else:

                    temp = article.split("LENGTH")
                    temp_ = temp[1].splitlines()
                
                    temp_c = 3

                    abstract = ""

                    while(not temp_[temp_c] == ''):
                        abstract = abstract + temp_[temp_c]
                        temp_c += 1
                                           
                if (abstract[-1] == ")"):
                    abstract = abstract[0:-3] 

                if day > 0 and day < 32 and month > 0 and month < 12:
                    date_time = datetime.date(year,month,day)
                    c.execute("INSERT INTO articles values (?, ?)", (date_time,abstract))
                    continue
                else:
                     raise ValueError('Not a month')
            except:

                try:
                    date_raw = article.splitlines(True)[5]

                    date = date_raw.replace(",","")
                    date_parts = date.split()

                    month = month_string_to_number(date_parts[0])
                    day = int(date_parts[1])
                    year = int(date_parts[2])

                   
                    if "ABSTRACT" in article.split("LENGTH")[1]:

                        temp = article.split("ABSTRACT")
                        temp_ = temp[1].splitlines()
                
                        temp_c = 2

                        abstract = ""

                        while(not temp_[temp_c] == ''):
                            abstract = abstract + temp_[temp_c]
                            temp_c += 1
                                                                   
                    else:

                        temp = article.split("LENGTH")
                        temp_ = temp[1].splitlines()
                
                        temp_c = 3

                        abstract = ""

                        while(not temp_[temp_c] == ''):
                            abstract = abstract + temp_[temp_c]
                            temp_c += 1
                
                           
                    if (abstract[-1] == ")"):
                        abstract = abstract[0:-3] 

                    #print(abstract)

                    if day > 0 and day < 32 and month > 0 and month < 12:
                        date_time = datetime.date(year,month,day)
                        c.execute("INSERT INTO articles values (?, ?)", (date_time,abstract))
                        continue
                    else:
                        raise ValueError('Not a month')

                except:
                      continue

                continue

        file.close()
        conn.commit()

        continue
    else:
        continue



conn.close()