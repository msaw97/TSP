import numpy as np

class Graf():
    """Reprezentacja grafu nieskierowanego w postaci macierzy sasiedztwa."""
    G = None
    n = 0

    def __init__(self, n):
        self.G = np.zeros((n,n))
        self.n = n

    def __repr__(self):
        return self.G

    def __str__(self):
        return str(self.G)

    def __getitem__(self, item):
        return self.G[item]

    def __iter__(self):
        for i in self.G:
            yield i

    def addE(self, u, v, w):
        """Dodaje krawedz z wierzcholka u do v z waga w."""
        if u != v:
            self.G[u-1][v-1] = w
            self.G[v-1][u-1] = w

    def removeE(self, u, v):
        """Usuwa krawedz z u do v"""
        self.addE(u,v, 0)

    def getWeight(self, u, v):
        """Zwraca wage krawedzi z wierzcholka u do v."""
        return self.G[u-1,v-1]

    def getRouteWeight(self, route):
        """Liczy sume wag krawedzi na sciezce"""
        routeWeight =[]

        for r in range(len(route)-1):
            routeWeight.append(self.getWeight(route[r], route[r+1]))

        return sum(routeWeight)


    def full_randomize(self):
        """Tworzy pelny graf z n wierzcholkow z losowymi wagami"""
        self.G = np.random.randint(1,100, self.G.shape)
        self.G = self.G + self.G.T  #tworzy macierz symetryczna
        np.fill_diagonal(self.G, 0)
        return self.G


if __name__ == "__main__":
    G = Graf(4)
    G.addE(1,2,2)
    G.addE(1,4,5)
    G.addE(3,3,4)
    G.removeE(1,4)
    print(G)
    print(G.getWeight(2,1))
    print(G.full_randomize())
