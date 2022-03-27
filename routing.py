import json
import math

import PriorityQueue


class WeightedGraph():
    def __init__(self):
        self.edges = {}

    def neighbour(self, nodeID):
        return list(self.edges.get(nodeID).keys())

    def cost(self, fromNodeID, toNodeID):
        return self.edges.get(fromNodeID).get(toNodeID)


def initGraph():
    nodeJson = open('data/nodes.json')
    edgeJson = open('data/edges.json')
    nodeDict = json.load(nodeJson)
    edgeDict = json.load(edgeJson)
    graph = WeightedGraph()
    for i in nodeDict["nodes"]:
        nodeedge = {}
        for j in edgeDict["edges"]:
            if i['nodeID'] == j['fromNode']:
                nodeedge.update({j['toNode']: j['cost']})

        graph.edges.update({i['nodeID']: nodeedge})
    return graph


def Hscore(fromNodeID, toNodeID):
    nodeJson = open('data/nodes.json')
    nodeDict = json.load(nodeJson)
    fromcord = []
    tocord = []
    for i in nodeDict["nodes"]:
        if (i['nodeID'] == fromNodeID):
            fromcord.append(i['latitude'])
            fromcord.append(i['longitude'])
        if (i['nodeID'] == toNodeID):
            tocord.append(i['latitude'])
            tocord.append(i['longitude'])
    latDis = math.radians(tocord[0] - fromcord[0])
    longDis = math.radians(tocord[1] - fromcord[1])
    a = pow(math.sin(latDis / 2), 2) + math.cos(math.radians(fromcord[0])) * math.cos(math.radians(tocord[0])) * \
        pow(math.sin(longDis / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    dis = (6371 * 1000) * c
    return dis


def findRoute(graph: WeightedGraph, startID, endID):
    pqueue = PriorityQueue.PriorityQueue()
    pqueue.enqueue(startID, 0)
    routeTable = {}
    GscoreTable = {}
    routeTable[startID] = None
    GscoreTable[startID] = 0

    while not pqueue.isEmpty():
        currentNode = pqueue.dequeue()
        if currentNode["ID"] == endID: return routeTable

        for i in graph.neighbour(currentNode["ID"]):
            Gscore = GscoreTable[currentNode["ID"]] + graph.cost(currentNode["ID"], i)
            if (i not in GscoreTable or Gscore < GscoreTable[i]):
                GscoreTable[i] = Gscore
                Fscore = Gscore + Hscore(i, endID)
                pqueue.enqueue(i, Fscore)
                routeTable[i] = currentNode["ID"]

    print("Path Not Found")
    return False


def reconstruct_path(routeTable, startID, endID):
    current = endID
    path = []
    while current != startID:  # note: this will fail if no path found
        path.append(current)
        current = routeTable[current]
    path.append(startID)
    path.reverse()
    return path


def route(startNodeID, endNodeID):
    graph = initGraph()
    resultRouteTable = findRoute(graph, startNodeID, endNodeID)
    if resultRouteTable:
        resultPath = reconstruct_path(resultRouteTable, startNodeID, endNodeID)
        # pathDict = {"path": resultPath}
        # print(resultPath)
        return resultPath
    else:
        return ["Path Not Found"]

def routewithtraffic(startNodeID,endNodeID):
    noTraffic = route(startNodeID,endNodeID)
    trafficX = int(len(noTraffic)/10)
    jamNode =[]
    for i in range(trafficX,-1,-1):
        jamNode.append(noTraffic[int(len(noTraffic)/2)-i])
    for i in range(1,trafficX+1):
        jamNode.append(noTraffic[int(len(noTraffic) / 2) + i])
    trafficGraph = initGraph()
    for x in range(1,len(jamNode)):
        trafficGraph.edges.get(jamNode[x-1])[jamNode[x]] *= 1000
    resultRouteTable = findRoute(trafficGraph, startNodeID, endNodeID)
    if resultRouteTable:
        resultPath = reconstruct_path(resultRouteTable, startNodeID, endNodeID)
        # pathDict = {"path": resultPath}
        # print(resultPath)
        return resultPath
    else:
        return ["Path Not Found"]



# !!! THIS LINE IS ONLY TO TEST IF ROUTING WORKS !!!
print(route(6542773042, 4600448914))
print(routewithtraffic(6542773042, 4600448914))
