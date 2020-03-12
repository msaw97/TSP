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

    print("routes:", routes)

    for r in routes:
        routeWeight = G.getRouteWeight(r)
        #print(routeWeight)
        if routeWeight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = routeWeight
            bestRoute = r

    return bestRoute, bestRouteWeight



G = Graf(4)
G.full_randomize()
print(G)

bR, bRW = brute_force(G)
print("\nNajkrotsza sciezka problemu TSP, metoda brute force: {}. Laczna waga krawedzi: {}.".format(bR, bRW))
