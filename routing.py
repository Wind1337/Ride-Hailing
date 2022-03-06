import json

nodeJson = open('data/nodes.json')
edgeJson = open('data/edges.json')
nodeDict= json.load(nodeJson)
edgeDict = json.load(edgeJson)

class WeightedGraph():
    def __init__(self):
        self.edges = {}

    def neighbour(self, nodeID):
        return self.edges.get(nodeID)

graph = WeightedGraph()
for i in nodeDict["nodes"]:
    nodeedge={}
    for j in edgeDict["edges"]:
        if i['nodeID'] == j['fromNode']:
            nodeedge.update({j['toNode']: j['cost']})

    graph.edges.update({i['nodeID']: nodeedge})

for i in nodeDict["nodes"]:
    print(graph.neighbour(i['nodeID']))





