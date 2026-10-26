from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.corpus import stopwords
import string
import json
import math
import time

app = Flask(__name__)
CORS(app) #allows page served from localhost:5500 to fetch from localhost:5000

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

invertedIndex   = load("data/invertedindex.json")
pageranks = load("data/pagerank.json")
df        = load("data/df.json")
documents = load("data/documents.json")
N         = load("data/doccount.json")["N"]

STOP_WORDS = set(stopwords.words("english"))    

@app.route("/api/query")
def search():
    start = time.perf_counter()
    query = request.args.get("q")

    keywords = str(query).lower()
    keywords = keywords.translate(str.maketrans(" ", " ", string.punctuation))
    tokens = keywords.split()
    pages = None
    idf = {}
    for token in tokens:
        if token not in STOP_WORDS and token.isalpha() and token in invertedIndex:
            if pages is None:
                pages = invertedIndex[token].keys()
            else:
                pages = pages&invertedIndex[token].keys()
            idf[token] = math.log(N/df[token]) 
    results = list(pages) if pages is not None else [] 

    rankings = {}
    for page in results:
        tf_idf = 0
        for token in tokens:
            if token not in STOP_WORDS and token.isalpha() and token in invertedIndex:
                tf = invertedIndex[token][page]
                tf_idf += tf * idf[token]
        rankings[page] = pageranks[page] * tf_idf

    results = sorted(results, key=lambda page: rankings[page], reverse=True)
    completeResults = [{"url": url, "title": documents[url]} for url in results]
    print((time.perf_counter() - start))
    return jsonify({"results": completeResults})  

if __name__ == "__main__":
    app.run(debug=True)