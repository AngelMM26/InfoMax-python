import numpy as np
from nltk.corpus import stopwords
import string
import unicodedata
import json

INVERTED_INDEX = {}
URL_FRQ = {}
DOC_URL = {}
ARTICLE_CONTENT = {}

STOP_WORDS = set(stopwords.words("english"))

def chunkText(text, chunkSize=180, overlap=30):
    words = text.split()
    chunks = []

    step = chunkSize - overlap
    for i in range(0, len(words), step):
        chunk = words[i:i + chunkSize]
        if chunk:
            chunks.append(" ".join(chunk))
    return chunks

def generateEmbeddings():
    #Imported lazily: loading sentence_transformers + the model takes ~1 min and would otherwise block startup
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")  # Load the pre-trained model for semantic retrieval
    embeddings = {}

    for url, chunks in ARTICLE_CONTENT.items():
        vectors = model.encode(
            chunks, 
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=True
        )  
        embeddings[url] = vectors

    return embeddings


def index(content, url):
    DOC_URL[url] = content.title.string

    #Removes extra content: scripts, navigation bars, menus, footers, ads, etc. 
    for tags in content(["script", "style", "header", "footer", "nav"]):
        tags.decompose()

    txt = content.get_text(separator=" ", strip=True) 

    #Removes control/format characters
    txt = ''.join(char for char in txt if unicodedata.category(char)[0] != "C")

    #Chunk article content for semantic retrieva
    ARTICLE_CONTENT[url] = chunkText(txt)

    #Removes punctuation, normalizes, lemmatizes, and tokenizes text
    txt = txt.translate(str.maketrans(" ", " ", string.punctuation))
    txt = txt.lower()
    tokens = txt.split()

    vistited = set()
    for token in tokens: #Maps token/terms to urls + includes term frequency 
        if token not in STOP_WORDS and token.isalpha():
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

    with open("data/articles.json", "w", encoding="utf-8") as file:
        json.dump(ARTICLE_CONTENT, file, ensure_ascii=False)

    print("Generating embeddings...")
    embeddings = generateEmbeddings()
    np.savez_compressed("data/embeddings.npz", **embeddings)






