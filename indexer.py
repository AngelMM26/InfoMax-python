from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import unicodedata
import json

INVERTED_INDEX = {}
URL_FRQ = {}
DOC_URL = {}

def index(content, url):
    DOC_URL[url] = content.title.string

    #Removes extra content: scripts, navigation bars, menus, footers, ads, etc. 
    for tags in content(["script", "style", "header", "footer", "nav"]):
        tags.decompose()

    txt = content.get_text(separator=" ") 

    #Removes control/format characters
    txt = ''.join(char for char in txt if unicodedata.category(char)[0] != "C")

    #Removes punctuation, normalizes, lemmatizes, and tokenizes text
    txt = txt.translate(str.maketrans(" ", " ", string.punctuation))
    txt = txt.lower()
    tokens = txt.split()
    stop_words = set(stopwords.words("english"))

    vistited = set()
    for token in tokens: #Maps token/terms to urls + includes term frequency 
        if token not in stop_words and token.isalpha():
            if token in INVERTED_INDEX:
                if url in INVERTED_INDEX[token]:
                    INVERTED_INDEX[token][url] += 1
                else:
                    INVERTED_INDEX[token][url] = 1
            else:
                frequency = {}
                frequency[url] = 1
                INVERTED_INDEX[token] = frequency   

            #Updates document frequency (df)
            if token not in vistited: 
                if token not in URL_FRQ:
                    URL_FRQ[token] = 1
                else:
                    URL_FRQ[token] += 1
                vistited.add(token)

def outputInfo(N):
    with open("data/invertedindex.json", "w", encoding="utf-8") as file:
        sortedIndex = dict(sorted(INVERTED_INDEX.items(), key=lambda x: x[0]))
        json.dump(sortedIndex, file, indent=2, ensure_ascii=False)

    with open("data/df.json", "w", encoding="utf-8") as file:
        sortedDF = dict(sorted(URL_FRQ.items(), key=lambda x: x[0]))
        json.dump(sortedDF, file, indent=2, ensure_ascii=False)

    with open("data/documents.json", "w", encoding="utf-8") as file:
        sortedDocs = dict(sorted(DOC_URL.items(), key=lambda x: x[0]))
        json.dump(sortedDocs, file, indent=2, ensure_ascii=False)

    with open("data/doccount.json", "w", encoding="utf-8") as file:
        json.dump({"N": N}, file, indent=2, ensure_ascii=False)






