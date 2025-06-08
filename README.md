# InfoMax 🔍

**InfoMax** is a lightweight search engine that crawls Wikipedia pages, indexes content using an inverted index, ranks results with PageRank, and serves them through a sleek frontend built with JavaScript and styled CSS. It's a complete end to end search engine implementation built from scratch using Python and Flask for the backend and vanilla JavaScript for the frontend. :)

---

## 📁 Project Structure

```
InfoMax/
│
├── crawler.py            # Crawls and collects pages from Wikipedia
├── indexer.py            # Builds the inverted index
├── rank.py               # Implements PageRank algorithm
├── server.py             # Flask backend to handle user search queries
├── main.html             # Search page interface
├── client.js             # Frontend JavaScript to fetch and render results
├── main.css              # CSS styling
├── df.json               # JSON file storing document frequency (df)
├── docCount.json         # JSON file storing number of documents
├── documents.json        # JSON file mapping URLS to website titles
├── invertedindex.json    # JSON file storing the inverted index
├── pagerank.json         # JSON file storing the PageRank scores
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Flask
- `nltk`, `beautifulsoup4`, `requests`

### Install Dependencies

```bash
pip install flask beautifulsoup4 requests nltk
```

---

## 🧠 How It Works

### 1. **Crawling**
- `crawler.py` uses BeautifulSoup and `requests` to crawl Wikipedia articles starting from a seed URL.
- It extracts internal Wikipedia links and visits them up to a defined `CRAWL_LIMIT`.

### 2. **Indexing**
- `indexer.py` tokenizes and preprocesses the content of crawled pages.
- It builds an inverted index mapping terms to a set of URLs containing them.
- The index is stored in `invertedindex.json`.

### 3. **Ranking**
- `rank.py` implements the **PageRank** algorithm.
- Pages with more inbound links from other high ranked pages are scored higher.
- Results are saved to `pagerank.json`.

### 4. **Search Interface**
- Users enter a query into the search bar in `index.html`.
- JavaScript (`client.js`) sends the query to the Flask backend.
- Flask (`server.py`) processes the query, retrieves matching documents, ranks them, and sends the results back to the frontend.
- Links are displayed dynamically in the browser.

---

## 🔎 Query Flow

1. **Preprocessing**: Stopwords are removed, punctuation is stripped, and text is lowercased.
2. **Intersection**: Only documents that match _all_ query tokens are returned.
3. **Ranking**: Results are sorted in descending order of PageRank.

---

## 🌐 Running the Project

1. Run the crawler (if not satisfied with sample data, may take a bit to run depending on desired CRAWL_LIMIT):

```bash
python crawler.py
```

2. Start the Flask server:

```bash
python server.py
```

3. Open `index.html` in your browser (hosted locally or using Live Server in VSCode).

---

## 💡 Features

- Custom web crawler for Wikipedia
- Inverted index for efficient keyword lookup
- PageRank scoring system
- Flask based backend API
- Clean, responsive search interface using JavaScript and CSS

---

## 📌 Future Enhancements

- Add support for **tf-idf** to improve ranking relevance ✅
- Incorporate **stemming** or **lemmatization** to improve indexing efficiency and reduce redundancy
- Introduce **multi-threaded crawling** for speed
- Use a database like **MongoDB** or **SQLite** for better scalability

---

## 🧑‍💻 Author

Angel Mejia Martinez  
Computer Science Major, NYU  
[LinkedIn](https://www.linkedin.com/in/angel-mejia-martinez-3b0a09252/) · [GitHub](https://github.com/AngelMM26)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
