import numpy as np
from itertools import permutations
import Graf
import time

def brute_force(G):
    """Rozwiazuje TSP metoda sprawdzenia wszyskich mozliwosci"""
    bestRoute = None
    bestRouteWeight = 0
    routes = list(permutations(range(1, G.n+1)))    #znajduje wszyskie n permutacji wierzcholkow
    routes = [ list(n) for n in routes]

    for n in routes:    #laczy sciezki w cykle
        n.append(n[0])

    for r in routes:
        routeWeight = G.getRouteWeight(r)
        if routeWeight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = routeWeight
            bestRoute = r

    return bestRoute, bestRouteWeight


#co jesli dwie krawedzie maja ta sama wage?
def nearest_neighbour(G):
    bestRoute = [0 for n in range(G.n)]
    current = 0
    visited = [current]

    for i in range(G.n):

        minimum = (0, 0)
        for j in range(len(G[current])):

            if j not in visited and  (0 < G[current][j] < minimum[0] or minimum == (0,0)):
                minimum = (G[current][j], j)

        current = minimum[1]
        bestRoute[i] = (visited[-1] +1, current +1)
        visited.append(minimum[1])

    bestRoute = [n[0] for n in bestRoute]
    bestRoute.append(bestRoute[0])

    return bestRoute

def smallest_edge(G):
    queue = []
    bestRoute = []

    #tworzy liste krawedzi wraz z ich wagami
    for n in range(0, G.n -1):
        min = [n+1, 0, G[n][n+1]]
        for j, k in enumerate( G[n][n+1:], n):
            min[1] = j+2
            min[2] = k
            queue.append(tuple(min))

    #sortowanie kolejki rosnaco wedlug wag
    queue = sorted(queue, key = lambda x: x[2])

    #sprawdza czy dołączenie tej krawędzi do rozwiązania nie spowoduje utworzenia cyklu i tworzy rozwiazanie
    while len(bestRoute) != G.n:
        edge = queue.pop(0)
        if edge[0] not in bestRoute:
            bestRoute.append(edge[0])
        if edge[1] not in bestRoute:
            bestRoute.append(edge[1])

    #przesuwa liste rozwiazania tak aby wierzcholek 1 znalazl sie na jej poczatku
    while bestRoute[0] != 1:
        bestRoute = [bestRoute[-1]] + bestRoute[:-1]

    bestRoute.append(bestRoute[0])

    return bestRoute

G = Graf.Graf(7)
G.full_randomize()

print("Najkrotsza sciezka problemu TSP.")
start =   time.time()
bR_BF, bRW_BF = brute_force(G)
print("Algorytm typu brute force: {}. Laczna waga krawedzi: {}.".format(bR_BF, bRW_BF))

bR_NN = nearest_neighbour(G)
bRW_NN = G.getRouteWeight(bR_NN)
print("Algorytm najblizszego sasiada: {}. Laczna waga krawedzi: {}.".format(bR_NN, bRW_NN))

bR_SE = smallest_edge(G)
bRW_SE = G.getRouteWeight(bR_SE)
print("Algorytm najmniejszej krawedzi: {}. Laczna waga krawedzi: {}.".format(bR_SE, bRW_SE))
