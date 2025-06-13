from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.corpus import stopwords
import string
import json
import math

app = Flask(__name__)
CORS(app) #allows page served from localhost:5500 to fetch from localhost:5000

with open("data/invertedindex.json", encoding="utf-8") as file:
    rawIndex = json.load(file)
    invertedIndex = {term: set(links) for term, links in rawIndex.items()}
    invertedIndex_tf = {term: links for term, links in rawIndex.items()}
    
with open("data/pagerank.json", encoding="utf-8") as file:
    pageranks = json.load(file)

with open("data/df.json", encoding="utf-8") as file:
    df = json.load(file)

with open("data/documents.json", encoding="utf-8") as file:
    documents = json.load(file)

with open("data/doccount.json", encoding="utf-8") as file:
    N = json.load(file)["N"]
    

@app.route("/search")
def search():
    query = request.args.get("q") 
    keywords = str(query).lower()
    keywords = keywords.translate(str.maketrans(" ", " ", string.punctuation))
    tokens = keywords.split()
    stop_words = set(stopwords.words("english"))
    pages = ""
    idf = {}
    for token in tokens:
        if token not in stop_words and token.isalpha() and token in invertedIndex:
            if pages == "":
                pages = invertedIndex[token]
            else:
                pages = pages&invertedIndex[token]
            idf[token] = math.log(N/df[token])           
    results = list(pages)
    rankings = {}
    for page in results:
        tf_idf = 0
        for token in tokens:
            if token not in stop_words and token.isalpha() and token in invertedIndex:
                tf = invertedIndex_tf[token][page]
                tf_idf += tf * idf[token]
        rankings[page] = pageranks[page] * tf_idf
    results = sorted(results, key=lambda page: rankings[page], reverse=True)
    completeResults = [{"url": url, "title": documents[url]} for url in results]
    return jsonify({"results": completeResults})  

if __name__ == "__main__":
    app.run(debug=True)