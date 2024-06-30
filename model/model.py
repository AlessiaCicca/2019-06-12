import copy

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
    def getBestPath(self,  numeroGiocatori):
        self._soluzione = []
        self._costoMigliore = 0
        battuti=[]
        for nodo in self.grafo.nodes:
            parziale = [nodo]
            for arcoUscente in self.grafo.out_edges(nodo):
                battuti.append(arcoUscente[1])
            self._ricorsione(parziale,numeroGiocatori,battuti)
        return self._costoMigliore,self._soluzione

    def _ricorsione(self, parziale, numeroGiocatori,battuti):
        if len(parziale) == numeroGiocatori:
            if self.grado(parziale)>self._costoMigliore:
                self._soluzione=copy.deepcopy(parziale)
                self._costoMigliore=self.grado(parziale)

        if len(parziale)<numeroGiocatori:
            for n in self.grafo.nodes:
                if n not in parziale and n not in battuti:
                    parziale.append(n)
                    for arcoUscente in self.grafo.out_edges(n):
                        battuti.append(arcoUscente[1])
                    self._ricorsione(parziale,numeroGiocatori,battuti)
                    parziale.pop()
                    for arcoUscente in self.grafo.out_edges(n):
                        battuti.remove(arcoUscente[1])
    def grado(self, listaNodi):
        gradoTot = 0
        for nodo in listaNodi:
            pesoUscente=0
            pesoEntrante=0
            for arcoUscente in self.grafo.out_edges(nodo):
                pesoUscente+= self.grafo[arcoUscente[0]][arcoUscente[1]]["weight"]
            for arcoEntrante in self.grafo.in_edges(nodo):
                pesoEntrante+=self.grafo[arcoEntrante[0]][arcoEntrante[1]]["weight"]
            gradoTot+=pesoUscente-pesoEntrante
        return gradoTot


