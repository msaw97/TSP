# -*- coding: utf-8 -*-
#Autor: Miłosz Sawicki
#Licencja: GNU GPL


import numpy as np
from itertools import permutations, combinations
import graphs


def brute_force(G):
    """Rozwiązuje TSP metodą sprawdzenia wszystkich możliwości."""
    bestPath = None
    bestPathWeight = 0
    paths = list(permutations(range(0, G.n)))    #znajduje wszystkie n permutacji wierzchołków
    paths = [list(n) for n in paths]

    for n in paths:    #łączy ścieżki w cykle
        n.append(n[0])

    for r in paths:
        temp_weight = G.get_path_weight(r)
        if temp_weight < bestPathWeight or bestPathWeight == 0:
            bestPathWeight = temp_weight
            bestPath = r

    return bestPath, bestPathWeight


def shift_right(lst):
    return lst[1:] + [lst[0]]


def nearest_neighbour(G, current):
    """Algorytm najbliższego sąsiada."""
    bestPath = [0 for n in range(G.n)]
    visited = [current]

    for i in range(G.n):

        #znajduje najkrótszą spośród krawędzi łączących aktualny wierzchołek
        #z jeszcze nieodwiedzonymi wierzchołkami
        minimum = (0, 0)
        for j in range(len(G[current])):

            if j not in visited and \
            (0 < G[current][j] < minimum[0] or \
            minimum == (0,0)):
                    
                minimum = (G[current][j], j)

        current = minimum[1]
        bestPath[i] = (visited[-1], current)
        visited.append(minimum[1])

    bestPath = [n[0] for n in bestPath]
    bestPath.append(bestPath[0])

    return bestPath


def repeated_nearest_neighbour(G):
    """Powtarzalny algorytm najbliższego sąsiada (RNN)."""
    bestPath = None
    bestPathWeight = 0

    for n in range(G.n-1):
        temp_path = nearest_neighbour(G, n)
        temp_weight = G.get_path_weight(temp_path)

        if temp_weight < bestPathWeight or bestPathWeight == 0:
            bestPathWeight = temp_weight
            bestPath = temp_path

    return bestPath, bestPathWeight


def smallest_edge(G):
    """Algorytm najmniejszej krawędzi."""
    queue = []
    bestPath = []

    #Tworzona jest lista krawędzi wraz z ich wagami.
    #Krawędzie nie powtarzaja się tj. nie wystepuje krawedz (a,b,w) i (b,a,w).
    for n in range(0, G.n -1):
        minimum = [n, G[n][n], G[n][n+1]]     #[wiersz, kolumna, waga]
        for j, k in enumerate( G[n][n+1:], n):
            minimum[1] = j+1
            minimum[2] = k
            queue.append(graphs.Edge(*minimum))

    #Sortowanie kolejki rosnaco według wag.
    queue.sort(key = lambda x: x.w)

    #Tworzony jest graf zaimplementowany przez liste sąsiedztwa, zawierący tylko wierzchołki.
    solution = graphs.GraphAdjacencyList(G.n)

    edge_count = 0
    for i in range(len(queue)):
        edge = queue.pop(0)

        #Dodawanie krawędzi w ostatnej iteracji algorytmu.
        if edge_count == G.n-1 and solution.is_not_third(edge.u.key, edge.v.key):
            solution.add_edge(edge.u.key, edge.v.key)

        #Dodawanie krawędzi, gdy nie powstanie wierzchołek,
        #z którego wychodzą trzy krawędzie oraz nie powstanie cykl.
        elif solution.is_not_third(edge.u.key, edge.v.key) and \
        solution.has_cycle(edge.u.key, edge.v.key) == False:
            solution.add_edge(edge.u.key, edge.v.key)
            edge_count += 1

    return solution.get_path()


def held_karp(G):
    """Algorytm Helda-Karpa"""

    #D - słownik reprezentujący długość ścieżki wychodzącej od wierzchołka 0 do p,
    #która przechodzi przez te wierzchołki w grafie określone zbiorem S.
    #Kluczem D jest krotka (S, p).
    #Wartością D jest krotka (y, p), w której
    #y - suma wag krawędzi na ścieżce, p - indeks przedostatniego wierzchołka na ścieżce.
    
    D = {}

    #Do rozwiązania dodawane są przypadki trywialne, gdzie zbiór S jest jednoelementowy.
    for j in range(1, G.n):
        D[(j, j)] = (G.get_edge_weight(0, j), 0)

    #Zmienna subset_size oznacza ilość elementów w zbiorze S.
    for subset_size in range(2, G.n):

        #Poniższa pętla iteruje po możliwych kombinacjach wierzchołków w zbiorze S 
        #dla konkretnej wartości subset_size
        print("kombinacje:", list(combinations(range(1,G.n), subset_size)))
        for subset in combinations(range(1,G.n), subset_size):
            for p in subset:

                path = [0]
                prev = 0
                for i, n in enumerate(subset):

                    if n == p:
                        continue

                    #subset[i] to przedostatni wierzchołek na ścieżce.
                    prev = subset[i]
                    path.append(n)

                #Dodawany jest ostatni wierzchołek p.
                path.append(p)

                #Lista perm zawiera wszystkie możliwości ustawienia wierzchołków w pathx
                perm = []
                for l in permutations(path[1:-1], subset_size-1):

                    #Do listy perm dodawana jest suma wag krawędzi ścieżki oraz indeks przedostatniego wierzchołka.
                    perm.append((G.get_path_weight(path[:1] + list(l) + path[-1:]), l[-1]))

                print("path: {}, perm: {}".format(path,perm))

                #Do D dodawany jest element perm z najmniejszą sumą wag krawędzi.
                D[((subset), p)] = min(perm, key = lambda x: x[0])


    print("\nD:", D)
