from bs4 import BeautifulSoup
from urllib.parse import urlparse
from  indexer import index, outputInfo
from rank import pagerank
from concurrent.futures import ThreadPoolExecutor
import queue
import requests
import threading
import time
import random

CRAWL_LIMIT = 500   #Crawler might overcrawl by the number of threads
NUM_THREADS = 50

def crawl(args):
    urls = args["urls"]
    visited = args["visited"]
    crawls = args["crawls"]
    graph = args["graph"]
    lock = args["lock"]
    stopEvent = args["stopEvent"]

    while not stopEvent.is_set():
        try: 
            url = urls.get(timeout=5)  
        except queue.Empty:
            break
        
        with lock:
            if not crawls[0] < CRAWL_LIMIT:
                stopEvent.set()
                break
            if url in visited:
                continue
            #print("Crawling:", url)
            visited.add(url)
        time.sleep(random.uniform(1, 2.5))

        #HTTP GET request to the currURL in an attempt to retrieve data 
        try:
            response = requests.get(url)
            response.raise_for_status() 
        except requests.RequestException as err:
            print(f"Failed to retrieve {url}: {err}")
            continue
        
        webpage = response.text
        content = BeautifulSoup(webpage, "html.parser")
        index(content, url)
       
        links = content.findAll("a")
        connections = set()
        for link in links:
            try:
                #Attempt to filter out "utility" pages, i.e wiki/Wikipedia:Community_portal, wiki/Help:Introduction, /wiki/Special:Random
                if link["href"].startswith("/wiki") and ":" not in urlparse(link["href"]).path:
                    #reformat urls
                    link["href"] = "https://en.wikipedia.org" + link["href"]
                else:
                    continue
            #Some href attributes do not have a valid link
            except KeyError: 
                continue 
            connections.add(link["href"])
            urls.put(link["href"])
            
        with lock:
            crawls[0] += 1
            graph[url] = connections
    

def wikiBot():
    start = time.time()

    urls = queue.Queue()
    urls.put("https://en.wikipedia.org/wiki/New_York_City")
    visited = set()
    crawls = [0] #We do this b/c this is passed by value, not reference --> each thread will get its own copy and not a shared one
    graph = {}
    lock = threading.Lock()
    stopEvent = threading.Event() #Intially sets internal flag to False

    args = {
        "urls" : urls,
        "visited": visited, 
        "crawls": crawls,
        "graph" : graph,
        "lock" : lock,
        "stopEvent" : stopEvent
    }

    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        for _ in range(NUM_THREADS):
            executor.submit(crawl, args)

    pagerank(graph)
    outputInfo(len(visited))
    print(time.time() - start)

wikiBot()


        







