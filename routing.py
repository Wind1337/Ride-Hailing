import json
import math

import PriorityQueue

nodeJson = open('data/nodes.json')
edgeJson = open('data/edges.json')
nodeDict = json.load(nodeJson)
edgeDict = json.load(edgeJson)


class WeightedGraph():
    def __init__(self):
        self.edges = {}

    def neighbour(self, nodeID):
        return list(self.edges.get(nodeID).keys())

    def cost(self, fromNodeID, toNodeID):
        return self.edges.get(fromNodeID).get(toNodeID)


graph = WeightedGraph()
for i in nodeDict["nodes"]:
    nodeedge = {}
    for j in edgeDict["edges"]:
        if i['nodeID'] == j['fromNode']:
            nodeedge.update({j['toNode']: j['cost']})

    graph.edges.update({i['nodeID']: nodeedge})


def Hscore(fromNodeID, toNodeID):
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


print(Hscore(5184383632, 4592745095))
print(graph.cost(5184383632, 4592745095))


def routing(graph: WeightedGraph, startID, endID):
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
    path.append(startID)  # optional
    path.reverse()  # optional
    return path


# print(routing(graph,4700694098,9142407272))
resultRouteTable = routing(graph, 6542773042, 4600448914)
if resultRouteTable:
    resultPath = reconstruct_path(resultRouteTable, 6542773042, 4600448914)
    pathDict = {"path": resultPath}
    # print(resultPath)
else:
    pathDict = {"path": ["Path Not Found"]}

json_object = json.dumps(pathDict, indent=4)
with open("./output/route.json", "w") as outfile:
    outfile.write(json_object)
