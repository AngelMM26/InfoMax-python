from bs4 import BeautifulSoup
from urllib.parse import urlparse
from  indexer import index, outputInfo
from rank import pagerank
import requests
import time
import random

CRAWL_LIMIT = 500
N = 0 #Total documents  

def wikiBot():
    urls = ["https://en.wikipedia.org/wiki/New_York_City"]
    visited = set()
    crawls = 0

    graph = {}
    while urls and crawls < CRAWL_LIMIT:
        url = urls.pop(0)
        if url in visited:
            continue
        time.sleep(random.uniform(0.5, 1.5))

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
                    #print("Fetching: ", link["href"])
                    #reformat urls
                    link["href"] = "https://en.wikipedia.org" + link["href"]
                else:
                    continue
            #Some href attributes do not have a valid link
            except KeyError: 
                continue 

            connections.add(link["href"])

            if link["href"] not in visited:
                urls.append(link["href"])
            else: 
                continue
        crawls += 1
        graph[url] = connections
        visited.add(url)
        #print(visited)
    N = len(visited)
    pagerank(graph)
    outputInfo(N)
  
start = time.time()
wikiBot()
print(time.time() - start)


        







