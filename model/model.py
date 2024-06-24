import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo=nx.DiGraph()
        self.giocatori=DAO.getAllGiocatori()
        self._idMap = {}
        for v in self.giocatori:
            self._idMap[v.PlayerID] = v

    def creaGrafo(self, ngoal):
        self.nodi = DAO.getNodi(ngoal)
        self.grafo.add_nodes_from(self.nodi)
        self.addEdges()
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def addEdges(self):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni()
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    peso=connessione.t1-connessione.t2
                    if peso>0:
                        self.grafo.add_edge(nodo1, nodo2, weight=peso)
                    if peso<0:
                        self.grafo.add_edge(nodo2, nodo1, weight=abs(peso))

    def getTop(self):
        dizio={}
        lista=[]
        for nodo in self.grafo.nodes:
            dizio[nodo.PlayerID]=self.grafo.out_degree(nodo)
        dizioOrdinato=list(sorted(dizio.items(), key=lambda item:item[1], reverse=True))
        giocatoreId=dizioOrdinato[0][0]
        giocatore=self._idMap[giocatoreId]
        for archi in self.grafo.out_edges(giocatore):
            lista.append((archi[1],self.grafo[archi[0]][archi[1]]["weight"]))
        return giocatore,sorted(lista,key=lambda x:x[1],reverse=True)


