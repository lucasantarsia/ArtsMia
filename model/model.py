import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._artObjectList = DAO.getAllObjects()
        self._grafo = nx.Graph()
        self._grafo.add_nodes_from(self._artObjectList)

        self._idMap = {}
        for v in self._artObjectList:
            self._idMap[v.object_id] = v

        self._solBest = []
        self._pesoBest = 0

    def getConnessa(self, v0int):
        v0 = self._idMap[v0int]

        # Modo 1: successori di v0 in DFS
        successors = nx.dfs_successors(self._grafo, v0)  # -> mi ritorna un dizionario dei nodi successori del nodo source
        print(f"Metodo 1 (succ): {len(successors.values())}")
        # Facendo come sopra non conta tutti i successori, quindi scandiamo tutti i nodi con un for:

        allSucc = []
        for v in successors.values():
            allSucc.extend(v)  # extend(v): se ad esempio v è una lista, permette di aggiungere tutti gli elementi uno ad uno
        print(f"Metodo 1 (succ): {len(allSucc)}")

        # Modo 2: predecessori di v0 in DFS
        predecessors = nx.dfs_predecessors(self._grafo, v0)  # -> mi ritorna un dizionario dei nodi predecessori del nodo source
        print(f"Metodo 2 (prec): {len(predecessors.values())}")
        # La lunghezza non è la stessa di len(successors.value()), come mai?

        # Perché ogni elemento del dizionario dei predecessori è sempre 1, dato che il predecessore di un nodo è sempre uno solo.
        # Invece gli elementi del dizionario dei successori possono essere anche delle liste perché i successori di un nodo
        # possono anche essere più di uno. Il metodo len(successors.values()) conta quindi solo gli elementi del dizionario
        # e non conta tutti i nodi successori ma possiamo ovviare a questo facendo un ciclo for (vedi sopra)

        # Modo 3: conto i nodi dell'albero di visita
        tree = nx.dfs_tree(self._grafo, v0)  # -> restituisce un grafo (albero)
        print(f"Metodo 3 (tree): {len(tree.nodes)}")
        # Il modo 3 ci dà un valore in più di len(predecessors.values()) perché conta anche il nodo source

        # Modo 4: node_connected_component
        connComp = nx.node_connected_component(self._grafo, v0)  # -> restituisce un set di nodi
        print(f"Metodo 4 (connected comp): {len(connComp)}")

        return len(connComp)

    def creaGrafo(self):
        self.addEdges()

    def addEdges(self):
        self._grafo.clear_edges()

        # Soluzione 1: Ciclare sui nodi -> più facile da eseguire ma tipicamente più lento
        # for u in self._artObjectList:
        #     for v in self._artObjectList:
        #         peso = DAO.getPeso(u, v)
        #         self._grafo.add_edge(u, v, weight=peso)

        # Soluzione 2: una sola query
        allEdges = DAO.getAllConnessioni(self._idMap)
        for e in allEdges:
            self._grafo.add_edge(e.v1, e.v2, weight=e.peso)

    def getBestPath(self, lun, v0):
        self._solBest = []
        self._pesoBest = 0

        parziale = [v0]  # il vertice iniziale è v0

        for v in self._grafo.neighbors(v0):  # ciclo sui vicini di v0
            if v.classification == v0.classification:
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

        return self._solBest, self._pesoBest

    def ricorsione(self, parziale, lun):
        # Controllo se parziale è una sol valida, e in caso se è migliore del best
        if len(parziale) == lun:
            if self.peso(parziale) > self._pesoBest:
                self._pesoBest = self.peso(parziale)
                self._solBest = copy.deepcopy(parziale)
            return

        # Se arrivo qui, allora len(parziale) < lun, quindi devo continuare ad aggiungere
        for v in self._grafo.neighbors(parziale[-1]):
            # v lo aggiungo se non è già in parziale e se ha la stessa classification di v0
            if v.classification == parziale[-1].classification and v not in parziale:
            #  controllo che la classification sia la stessa e che v non sia già stato aggiunto
                parziale.append(v)
                self.ricorsione(parziale, lun)
                parziale.pop()

    def peso(self, listObject):  # Calcola il peso totale della lista di nodi vicini
        p = 0
        for i in range(0, len(listObject)-1):
            p += self._grafo[listObject[i]][listObject[i+1]]["weight"]
        return p

    def checkExistence(self, idOggetto):
        return idOggetto in self._idMap  # -> ritorna true se idOggetto è una chiave della mappa

    def getObjectFromId(self, idOggetto):  # -> prendo l'id dell'oggetto e mi ritorna l'oggetto
        return self._idMap[idOggetto]

    def getNumNodes(self):
        return len(self._grafo.nodes)

    def getNumEdges(self):
        return len(self._grafo.edges)
