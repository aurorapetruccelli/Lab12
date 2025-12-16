import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        """Definire le strutture dati utili"""
        self.lista_rifugi = []
        self.getRifugi()
        self._rifugi = {}
        #creo un dizionario con l'id del rifugio come chiave e come valore l'oggetto rifugio
        for rifugio in self.lista_rifugi:
            self._rifugi[rifugio.id] = rifugio

        self.G = nx.Graph()
        self.peso_minimo = 100000
        self.cammino_migliore = []
        self._cammino_da_stampare = []

    def getRifugi(self):
        self.lista_rifugi = DAO.read_rifugi()


    def build_weighted_graph(self, year: int):
        """
        Costruisce il grafo pesato dei rifugi considerando solo le connessioni con campo `anno` <= year passato
        come argomento.
        Il peso del grafo è dato dal prodotto "distanza * fattore_difficolta"
        """
        connessioni = DAO.read_connessioni(year)
        for connessione in connessioni:
            nodo1 = connessione._id_rifugio1
            nodo2 = connessione._id_rifugio2
            if connessione._difficolta == "facile":
                connessione._difficolta = 1
            elif connessione._difficolta == "media":
                connessione._difficolta = 1.5
            elif connessione._difficolta == "difficile":
                connessione._difficolta = 2

            peso = float(connessione._distanza) * float(connessione._difficolta)
            self.G.add_edge(nodo1, nodo2, weight=peso)

        print(self.G)
        return self.G



    def get_edges_weight_min_max(self):
        """
        Restituisce min e max peso degli archi nel grafo
        :return: il peso minimo degli archi nel grafo
        :return: il peso massimo degli archi nel grafo
        """
        lista_di_pesi = []
        for u, v in self.G.edges():
            peso = self.G[u][v]["weight"]
            lista_di_pesi.append(peso)

        massimo = max(lista_di_pesi)
        minimo = min(lista_di_pesi)

        print(f"Il massimo è {massimo}, il minimo è {minimo}")
        return minimo, massimo

    def count_edges_by_threshold(self, soglia):
        """
        Conta il numero di archi con peso < soglia e > soglia
        :param soglia: soglia da considerare nel conteggio degli archi
        :return minori: archi con peso < soglia
        :return maggiori: archi con peso > soglia
        """
        num_archi_soglia_minore = 0
        num_archi_soglia_maggiore = 0
        for u, v in self.G.edges():
            peso = self.G[u][v]["weight"]
            if soglia > peso:
                num_archi_soglia_minore += 1
            elif soglia < peso:
                num_archi_soglia_maggiore += 1

        print(f"{num_archi_soglia_minore}, {num_archi_soglia_maggiore}")
        return num_archi_soglia_minore, num_archi_soglia_maggiore



    """Implementare la parte di ricerca del cammino minimo"""
    #metodo ricorsivo
    def calcolo_cammino_minimo(self,soglia):
        # inizializzo le variabili
        self.peso_minimo = 100000
        self.cammino_migliore = []
        self._cammino_da_stampare = []

        for nodo in self.G.nodes():
            self.ricorsione(nodo,[nodo],[],0,soglia)


        for lista in self.cammino_migliore:
            u, v ,peso = lista[0],lista[1],lista[2]
            rifugio1 = self._rifugi[u]
            rifugio2 = self._rifugi[v]
            #in questo modo posso stampare come rifugio1 e rifugio2 gli oggetti rifugio e non i singoli id
            self._cammino_da_stampare.append([rifugio1, rifugio2,peso])

        print(self._cammino_da_stampare)
        return self._cammino_da_stampare


    def ricorsione(self,nodo, visitati, cammino , peso, soglia):
        if len(cammino)>=2:
            # se ho più di due archi , la soluzione è valida
            if peso<self.peso_minimo:
                # se il peso è minore di peso_minimo lo salvo
                self.peso_minimo = peso
                self.cammino_migliore=cammino.copy()

        else:
            for vicino in self.G.neighbors(nodo):
                if vicino not in visitati:
                    # controllo se il vicino non è nei nodi visitati
                    peso_arco= float(self.G[vicino][nodo]["weight"])
                    if peso_arco>soglia:
                        # controllo se il peso tra i nodi è maggiore della soglia
                        visitati.append(vicino)
                        cammino.append([nodo,vicino,peso_arco])
                        self.ricorsione(vicino,visitati,cammino,peso+peso_arco,soglia)
                        cammino.pop()
                        visitati.remove(vicino)


"""
    # metodo shortest paths
    def calcolo_cammino_minimo(self,soglia):
        self.peso_minimo = 100000
        self.cammino_migliore = []
        self._cammino_da_stampare = []


        G = nx.Graph()
        #creo un nuovo grafo in cui inserisco solo gli archi con il peso maggiore di una soglia
        for u,v in self.G.edges():
            if self.G[u][v]["weight"] > soglia:
                G.add_edge(u, v, weight=self.G[u][v]["weight"])


        for nodo in G.nodes():
            peso,percorso = nx.single_source_dijkstra(G, nodo,weight = "weight")
            # ottengo due dizionari
            # il primo ha come chiavi il nodo di arrivo e come valori il peso totale
            # il secondo ha come chiavi il nodo di arrivo e come valore una lista
            # in cui sono presenti i nodi in cui passa per arrivare al nodo di arrivo
            for nodo_arrivo,nodi_intermedi in percorso.items():
                if len(nodi_intermedi)>=3:
                    # controllo che i nodi del percorso sono tre o più
                    peso_totale = peso[nodo_arrivo]
                    if peso_totale<self.peso_minimo:
                        #aggiorno i valori se sono minori del peso perchè voglio trovare il percorso con il peso minimo
                        self.peso_minimo=peso_totale
                        self.cammino_migliore = []
                        for i in range(len(nodi_intermedi)-1):
                            #aggiungo al cammino i nodi e il loro peso (quindi aggiungo gli archi)
                            self.cammino_migliore.append([nodi_intermedi[i],nodi_intermedi[i+1],G[nodi_intermedi[i]][nodi_intermedi[i+1]]["weight"]])

        for lista in self.cammino_migliore:
            u, v, peso = lista[0], lista[1], lista[2]
            rifugio1 = self._rifugi[u]
            rifugio2 = self._rifugi[v]
            self._cammino_da_stampare.append([rifugio1, rifugio2, peso])

        print(self._cammino_da_stampare)
        return self._cammino_da_stampare
"""
