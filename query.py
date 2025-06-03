from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.corpus import stopwords
import string
import json

app = Flask(__name__)
CORS(app) #allows page served from localhost:5500 to fetch from localhost:5000

with open("invertedindex.json", encoding="utf-8") as file:
    rawIndex = json.load(file)
    invertedIndex = {term: set(links) for term, links in rawIndex.items()}
    
with open("pagerank.json", encoding="utf-8") as file:
    pageranks = json.load(file)


@app.route("/search")
def search():
    query = request.args.get("q") 
    keywords = str(query).lower()
    keywords = keywords.translate(str.maketrans(" ", " ", string.punctuation))
    tokens = keywords.split()
    stop_words = set(stopwords.words("english"))
    pages = ""
    for token in tokens:
        if token not in stop_words and token.isalpha() and token in invertedIndex:
            if pages == "":
                pages = invertedIndex[token]
            else:
                pages = pages&invertedIndex[token]
    results = list(pages)
    results = sorted(results, key=lambda url: pageranks[url], reverse=True)
    return jsonify({"results": results})  

if __name__ == "__main__":
    app.run(debug=True)