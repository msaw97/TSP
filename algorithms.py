# -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 26.06.20
# Moduł zawierający implementacje algorytmów rozwiązujących problem komiwojażera.

import numpy as np
from itertools import permutations, combinations
import graphs

def brute_force(G):
    """Rozwiązuje TSP metodą sprawdzenia wszystkich możliwości.
    G jest pełnym grafem nieskierowanym w postaci macierzy sąsiedztwa.
    """

    # Zmienna pathWeight jest sumą wszystkich wag krawędzi ścieżki.
    pathWeight = 0

    # Znajdowane są wszystkie permutacje n wierzchołków.
    paths = list(permutations(range(0, G.n)))
    paths = [list(n) for n in paths]

    # Ścieżki łączone są w cykle.
    for n in paths:
        n.append(n[0])

    # Lista bestPath jest ścieżką o najmniejszym koszcie wszystkich krawędzi.
    for r in paths:
        temp_weight = G.get_path_weight(r)
        if temp_weight < pathWeight or pathWeight == 0:
            pathWeight = temp_weight
            bestPath = r

    return bestPath, pathWeight

def NN_ALG(G, current):
    """Algorytm najbliższego sąsiada.
    G jest pełnym grafem nieskierowanym w postaci macierzy sąsiedztwa.
    Zmienna current oznacza wierzchołek początkowy.
    """

    # Lista bestPath zawiera ścieżkę będącą rozwiązaniem;
    bestPath = [0 for n in range(G.n)]
    # Lista visited zawiera odwiedzone już wierzchołki;
    visited = [current]

    # Znajduje najkrótszą spośród krawędzi
    # łączących aktualny wierzchołek
    # z jeszcze nieodwiedzonymi wierzchołkami.
    for i in range(G.n):
        # Krotka minimum := (w, j) zawiera indeks jeszcze nieodwiedzonego
        # wierzchołka j oraz wagę krawędzi w, łączącą j z ostatnio dodanym
        # wierzchołkiem rozwiązania.
        minimum = (0, 0)
        for j in range(G.n):

            if (j not in visited and
            (0 < G[current][j] < minimum[0] or minimum == (0, 0))):
                minimum = (G[current][j], j)

        current = minimum[1]
        bestPath[i] = visited[-1]
        visited.append(current)

    # Ścieżka łączona jest w cykl
    bestPath.append(bestPath[0])

    return bestPath, G.get_path_weight(bestPath)

def RNN_ALG(G):
    """Powtarzalny algorytm najbliższego sąsiada (RNN).
    G jest pełnym grafem nieskierowanym w postaci macierzy sąsiedztwa.
    """

    # Lista bestPath zawiera ścieżkę o najmniejszej wadze z już sprawdzonych ścieżek.
    bestPath = None
    bestPathWeight = 0

    for i in range(G.n):
        # Wywoływany jest algorytm najbliższego sąsiada dla każdego n.
        temp_path, temp_weight = NN_ALG(G, i)

        # Porównywana jest obecna najlepsza ścieżka z nowym rozwiązaniem.
        if temp_weight < bestPathWeight or bestPathWeight == 0:
            bestPathWeight = temp_weight
            bestPath = temp_path

    return bestPath, bestPathWeight

def CI_ALG(G):
    """Algorytm najmniejszej krawędzi (ang. cheapest insertion algorithm)
    G jest pełnym grafem nieskierowanym w postaci macierzy sąsiedztwa.
    """

    # queue - lista krawędzi wraz z ich wagami;
    # Krawędzie nie powtarzaja się tj. nie wystepuje krawedz (a,b,w) i (b,a,w).
    queue = []
    for n in range(0, G.n-1):
        minimum = [n, G[n][n], G[n][n+1]]     # [wiersz, kolumna, waga]
        for j, k in enumerate(G[n][n+1:], n):
            minimum[1] = j+1
            minimum[2] = k
            queue.append(graphs.Edge(*minimum))

    # Sortowanie kolejki rosnaco według wag.
    queue.sort(key = lambda x: x.w)

    # Tworzony jest graf określony przez liste sąsiedctwa zawierający rozwiązanie.
    solution = graphs.GraphAdjacencyList(G.n)

    edge_count = 0
    for i in range(len(queue)):
        edge = queue.pop(0)

        # Dodawanie krawędzi w ostatnej iteracji algorytmu.
        if edge_count == G.n-1 and solution.is_not_third(edge.u.key, edge.v.key):
            solution.add_edge(edge.u.key, edge.v.key)

        # Dodawanie krawędzi, gdy nie powstanie wierzchołek,
        # z którego wychodzą trzy krawędzie oraz nie powstanie cykl.
        elif (solution.is_not_third(edge.u.key, edge.v.key) and
        solution.has_cycle(edge.u.key, edge.v.key) is False):
            solution.add_edge(edge.u.key, edge.v.key)
            edge_count += 1

    # Metoda get_path zwraca ścieżkę w grafie określonym przez listę sąsiedztwa.
    bestPath = solution.get_path()

    return bestPath,  G.get_path_weight(bestPath)



def held_karp(G):
    """Algorytm Helda-Karpa
    G jest pełnym grafem nieskierowanym w postaci macierzy sąsiedztwa.
    """

    # D jest słownikiem w postaci D[S, p] : (y, parent), gdzie
    # S - zbiór wierzchołków przez które przechodzi ścieżka bez wierzchołka 0;
    # p - ostatni wierzchołek przez który przechodzi ścieżka; 
    # y - suma wszystkich wag krawędzi na ścieżce;
    # parent - indeks przedostatniego wierzchołka na ścieżce.
    D = {}

    # Do rozwiązania dodawane są przypadki trywialne, gdzie zbiór S jest jednoelementowy.
    for j in range(1, G.n):
        D[((j,),j)] = (G.get_edge_weight(0, j), 0)

    # Zmienna subset_size oznacza ilość elementów w zbiorze S.
    for subset_size in range(2, G.n):
        for subset in combinations(range(1,G.n), subset_size):

            for p in subset:
                S_bez_p = [s for s in subset if s != p]
                path_weights = []

                for n in S_bez_p:
                    if (tuple(S_bez_p), n) in D.keys():
                        path_weights.append((D[(tuple(S_bez_p), n)][0] + G[n][p], n))

                D[tuple(subset),p] = (min(path_weights)[0], min(path_weights)[1])

    # Obliczanie kosztu przejścia całej ścieżki.
    cost = []
    S = tuple(range(1, G.n))

    for n in S:
        cost.append((D[(S,n)][0] + G[n][0], n))

    opt = (min(cost)[0], min(cost)[1])

    # Otwarzanie trasy korzystając z zmiennej parent.
    path = [0, opt[1]]
    parent = path[1]

    for i in reversed(sorted( D.items(), key = lambda x: len(x))):
        if i[0][0] == S and i[0][1] == parent:
            S = tuple([j for j in i[0][0] if j != i[0][1]])
            parent = i[1][1]
            path.append(parent)

    return path, opt[0]