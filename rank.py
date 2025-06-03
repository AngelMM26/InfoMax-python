import json

def pagerank(graph, damping=0.85, iterations=100):
    nodes = set(graph.keys())
    for outlinks in graph.values():
        nodes.update(outlinks)
    N = len(nodes)

    #Build incoming link graph, reverse of graph
    reverseGraph = {node: [] for node in nodes}
    for src, outlinks in graph.items():
        for out in outlinks:
            reverseGraph[out].append(src)

    #Initialize rankings
    rank = {url : 1/N for url in nodes}
    #Nodes with no outgoing links or that have not been crawled
    sinks = [url for url in nodes if url not in reverseGraph or len(graph.get(url,[])) == 0]
    for i in range(iterations):
        bestRank = {}
        #Redistribute rank from sinks equally to all nodes during each iteration
        sinkSum = sum(rank[sink] for sink in sinks)/N
        for node in nodes:
            sumPR = 0
            for inlink in reverseGraph[node]:
                numOutgoing = len(graph[inlink])
                if numOutgoing > 0:
                    currRank = rank[inlink]
                    sumPR += currRank/numOutgoing
            bestRank[node] = (1-damping)/N + damping*(sumPR+sinkSum)
        rank = bestRank
  
    with open("pagerank.json", "w", encoding="utf-8") as file:
        sortedRank = dict(sorted(rank.items(), key=lambda x: -x[1]))
        json.dump(sortedRank, file, indent=2, ensure_ascii=False)
    