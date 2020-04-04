# -*- coding: utf-8 -*-

import numpy as np
from itertools import permutations
import Graf
import time

def brute_force(G):
    """Rozwiazuje TSP metoda sprawdzenia wszyskich mozliwosci"""
    bestRoute = None
    bestRouteWeight = 0
    routes = list(permutations(range(1, G.n+1)))    #znajduje wszyskie n permutacji wierzcholków
    routes = [ list(n) for n in routes]

    for n in routes:    #łaczy ścieżki w cykle
        n.append(n[0])

    for r in routes:
        routeWeight = G.getRouteWeight(r)
        if routeWeight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = routeWeight
            bestRoute = r

    return bestRoute, bestRouteWeight

def shift_right(list):
    return list[1:] + [list[0]]


#co jeśli dwie krawedzie mają tą sama wage?
def nearest_neighbour(G, current):
    bestRoute = [0 for n in range(G.n)]
    visited = [current]

    for i in range(G.n):

        #znajduje najkrótszą spośród krawędzi łączących aktualny wierzchołek z jeszcze nieodwiedzonymi wierzchołkami
        minimum = (0, 0)
        for j in range(len(G[current])):

            if j not in visited and  (0 < G[current][j] < minimum[0] or minimum == (0,0)):
                minimum = (G[current][j], j)

        current = minimum[1]
        bestRoute[i] = (visited[-1] +1, current +1)
        visited.append(minimum[1])

    bestRoute = [n[0] for n in bestRoute]

    #if bestRoute[0] != 1:
    #    shift_right(bestRoute)

    bestRoute.append(bestRoute[0])

    return bestRoute

def smallest_edge(G):
    queue = []
    bestRoute = []

    #tworzy listę krawędzi wraz z ich wagami
    for n in range(0, G.n -1):
        min = [n+1, 0, G[n][n+1]]
        for j, k in enumerate( G[n][n+1:], n):
            min[1] = j+2
            min[2] = k
            queue.append(tuple(min))

    #sortowanie kolejki rosnaco według wag
    queue = sorted(queue, key = lambda x: x[2])

    #sprawdza czy dołączenie tej krawędzi do rozwiązania nie spowoduje utworzenia cyklu i tworzy rozwiazanie
    while len(bestRoute) != G.n:
        edge = queue.pop(0)
        if edge[0] not in bestRoute:
            bestRoute.append(edge[0])
        if edge[1] not in bestRoute:
            bestRoute.append(edge[1])

    #przesuwa liste rozwiazania tak aby wierzcholek 1 znalazł sie na jej poczatku
    while bestRoute[0] != 1:
        bestRoute = shift_right(bestRoute)

    bestRoute.append(bestRoute[0])

    return bestRoute

def RNN(G):
    """Powtarzalny algorytm najblizszego sasiada"""
    bestRoute = None
    bestRouteWeight = 0

    for n in range(G.n-1):
        temp_route = nearest_neighbour(G, n)
        temp_weight = G.getRouteWeight(temp_route)

        #print(temp_route)
        if temp_weight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = temp_weight
            bestRoute = temp_route

    return bestRoute, bestRouteWeight


G = Graf.Graf(7)
G.full_randomize()

print("Najkrótsza scieżka problemu TSP.")
start_time = time.time()
bR_BF, bRW_BF = brute_force(G)
final_time = time.time() - start_time
print("Algorytm typu brute force: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_BF, bRW_BF, final_time))

start_time = time.time()
bR_NN = nearest_neighbour(G, 0)
final_time = time.time() - start_time
bRW_NN = G.getRouteWeight(bR_NN)
print("Algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_NN, bRW_NN, final_time))

start_time =   time.time()
bR_SE = smallest_edge(G)
final_time = time.time() - start_time
bRW_SE = G.getRouteWeight(bR_SE)
print("Algorytm najmniejszej krawędzi: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}".format(bR_SE, bRW_SE, final_time))

start_time =   time.time()
bR_RNN, bRW_RNN = RNN(G)
final_time = time.time() - start_time
print("Powtarzalny algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_RNN, bRW_RNN, final_time))
