import numpy as np
from itertools import permutations
from Graf import Graf

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
    visited = [0]

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

G = Graf(8)
G.full_randomize()
print(G)

bR_BF, bRW_BF = brute_force(G)
print("\nNajkrotsza sciezka problemu TSP, metoda brute force: {}. Laczna waga krawedzi: {}.".format(bR_BF, bRW_BF))

bR_NN = nearest_neighbour(G)
bRW_NN = G.getRouteWeight(bR_NN)
print("\nNajkrotsza sciezka problemu TSP, metoda najblizszego sasiada: {}. Laczna waga krawedzi: {}.".format(bR_NN, bRW_NN))
