# -*- coding: utf-8 -*-

import numpy as np
from itertools import permutations
import Graf
import time

def brute_force(G):
    """Rozwiazuje TSP metoda sprawdzenia wszyskich mozliwosci"""
    bestRoute = None
    bestRouteWeight = 0
    routes = list(permutations(range(0, G.n)))    #znajduje wszyskie n permutacji wierzcholków
    routes = [ list(n) for n in routes]

    for n in routes:    #łączy ścieżki w cykle
        n.append(n[0])

    for r in routes:
        temp_weight = G.getRouteWeight(r)
        if temp_weight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = temp_weight
            bestRoute = r

    return bestRoute, bestRouteWeight


def shift_right(lst):
    return lst[1:] + [lst[0]]


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
        bestRoute[i] = (visited[-1], current)
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
    #krawędzie nie powtarzaja się tj. nie wystepuje krawedz (a,b,w) i (b,a,w)
    for n in range(0, G.n -1):
        minimum = [n, G[n][n], G[n][n+1]]     #[wiersz, kolumna, waga]
        for j, k in enumerate( G[n][n+1:], n):
            minimum[1] = j+1
            minimum[2] = k
            queue.append(Graf.Edge(*minimum))

    #sortowanie kolejki rosnaco według wag
    queue.sort(key = lambda x: x.w)

    solution = Graf.Graf_adjlist(G.n )

    edge_count = 0
    for i in range(len(queue)):
        edge = queue.pop(0)

        #dodaje krawedz w ostatnej iteracji algorytmu
        if edge_count == G.n-1 and solution.is_not_third(edge.u.key, edge.v.key):
            solution.add_edge(edge.u.key, edge.v.key)

        #dodaje krawędź, gdy nie powstanie wierzchołek, z którego wychodzą trzy krawędzie oraz nie powstanie cykl
        elif solution.is_not_third(edge.u.key, edge.v.key) and solution.has_cycle(edge.u.key, edge.v.key) == False:
            solution.add_edge(edge.u.key, edge.v.key)
            edge_count += 1

    #solution.print_graph()
    return solution.get_path()


def RNN(G):
    """Powtarzalny algorytm najbliższego sąsiada."""
    bestRoute = None
    bestRouteWeight = 0

    for n in range(G.n-1):
        temp_route = nearest_neighbour(G, n)
        temp_weight = G.getRouteWeight(temp_route)

        if temp_weight < bestRouteWeight or bestRouteWeight == 0:
            bestRouteWeight = temp_weight
            bestRoute = temp_route

    return bestRoute, bestRouteWeight


G = Graf.Graf(7)
G.full_randomize()
#G.TEST()

print("Najkrótsza scieżka problemu TSP.")
print(G)

start_time = time.time()
bR_BF, bRW_BF = brute_force(G)
final_time = time.time() - start_time
print("\nAlgorytm typu brute force: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_BF, bRW_BF, final_time))

start_time = time.time()
bR_NN = nearest_neighbour(G, 0)
final_time = time.time() - start_time
bRW_NN = G.getRouteWeight(bR_NN)
print("\nAlgorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_NN, bRW_NN, final_time))

start_time =   time.time()
bR_SE = smallest_edge(G)
final_time = time.time() - start_time
bRW_SE = G.getRouteWeight(bR_SE)
print("\nAlgorytm najmniejszej krawędzi: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}".format(bR_SE, bRW_SE, final_time))

start_time =   time.time()
bR_RNN, bRW_RNN = RNN(G)
final_time = time.time() - start_time
print("\nPowtarzalny algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_RNN, bRW_RNN, final_time))
