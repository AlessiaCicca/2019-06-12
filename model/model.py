import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo=nx.Graph()
        self._idMap = {}

    def creaGrafo(self, ngoal):
        self.nodi = DAO.getNodi(ngoal)
        self.grafo.add_nodes_from(self.nodi)
        #self.addEdges(*)
        for v in self.nodi:
            self._idMap[v.PlayerID] = v
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
