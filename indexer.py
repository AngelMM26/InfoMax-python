from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import string
import unicodedata
import json


INVERTED_INDEX = {}

def index(content, url):
    #Removes extra content: scripts, navigation bars, menus, footers, ads, etc. 
    for tags in content(["script", "style", "header", "footer", "nav"]):
        tags.decompose()

    txt = content.get_text(separator=" ") 

    #Removes control/format characters
    txt = ''.join(char for char in txt if unicodedata.category(char)[0] != "C")

    #Removes punctuation, normalizes, and tokenizes text
    txt = txt.translate(str.maketrans(" ", " ", string.punctuation))
    txt = txt.lower()
    tokens = txt.split()
    stop_words = set(stopwords.words("english"))
    for token in tokens:
        if token not in stop_words and token.isalpha():
            if token in INVERTED_INDEX:
                INVERTED_INDEX[token].add(url)
            else:
                INVERTED_INDEX[token] = {url}     

def outputIndex():
    convertedIndex = {term: list(pages) for term, pages in INVERTED_INDEX.items()}
    with open("invertedindex.json", "w", encoding="utf-8") as file:
        sortedIndex = dict(sorted(convertedIndex.items(), key=lambda x: x[0]))
        json.dump(sortedIndex, file, indent=2, ensure_ascii=False)






