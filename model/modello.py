import copy

from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.idMap = {}

        self.maxPath = []

        self.bestPath = []
        self.bestScore = 0

    def getStoresID(self):
        return DAO.getStoresID()

    def buildGraph(self, store_id, days):
        nodes = DAO.getOrdersByStoreID(store_id)
        for n in nodes:
            self.idMap[n.order_id] = n
        self._graph.add_nodes_from(nodes)
        edges = DAO.getEdges(store_id, days, self.idMap)
        for e in edges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getNodes(self):
        return list(self._graph.nodes())

    def percorsoMassimo(self, start):
        self.maxPath = []

        parziale = [start]
        self.ricMax(parziale)

        return self.maxPath

    def ricMax(self, parziale):
        rimanenti = []
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                rimanenti.append(n)

        if len(rimanenti) == 0:
            if len(parziale) > len(self.maxPath):
                self.maxPath = copy.deepcopy(parziale)

        else:
            for n in rimanenti:
                parziale.append(n)
                self.ricMax(parziale)
                parziale.pop()

    def cammino_ottimo(self, start):
        self.bestPath = []
        self.bestScore = 0

        parziale = [start]
        self.ricorsione(parziale)

        return self.bestPath, self.bestScore

    def ricorsione(self, parziale):
        rimanenti = []
        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                rimanenti.append(n)
        if len(rimanenti) == 0:
            if self.calcola_score(parziale) > self.bestScore:
                self.bestScore = self.calcola_score(parziale)
                self.bestPath = copy.deepcopy(parziale)
        else:
            for n in rimanenti:
                parziale.append(n)
                self.ricorsione(parziale)
                parziale.pop()

    def calcola_score(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._graph[parziale[i]][parziale[i+1]]['weight']
        return score