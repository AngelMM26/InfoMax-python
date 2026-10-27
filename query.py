from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
from rag import generateOverview
import string
import json
import math
import time
import numpy as np

app = Flask(__name__)
CORS(app) #allows page served from localhost:5500 to fetch from localhost:5000

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

invertedIndex = load("data/invertedindex.json")
pageranks = load("data/pagerank.json")
df = load("data/df.json")
documents = load("data/documents.json")
N = load("data/doccount.json")["N"]
articles = load("data/articles.json")

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
EMBEDDINGS = np.load("data/embeddings.npz", allow_pickle=False)

STOP_WORDS = set(stopwords.words("english"))    

def retrieve(query):
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
    return [{"url": url, "title": documents[url]} for url in results]

def retrievePassages(query, top, topK=8):
    queryVector = MODEL.encode(
        query,
        normalize_embeddings=True
    )

    passages = []
    for url in top:
        chunks = articles[url]
        vectors = EMBEDDINGS[url]

        similarities = vectors @ queryVector #dot product

        for i, score in enumerate(similarities): 
            passages.append({
                "url": url,
                "chunk": chunks[i],
                "score": float(score)
            })

    passages.sort(key=lambda x: x["score"], reverse=True)
    return passages[:topK]

@app.route("/api/query")
def search():
    start = time.perf_counter()
    query = request.args.get("q")
    aiEnabled = request.args.get("aiEnabled") == "true"

    results = retrieve(query)
    response = {"results": results}

    if aiEnabled:
        topUrls = [result["url"] for result in results[:5]]
        passages = retrievePassages(query, topUrls)
        response["ai_answer"] = generateOverview(query, passages)

    print((time.perf_counter() - start))
    return jsonify(response)  

if __name__ == "__main__":
    app.run(debug=True)