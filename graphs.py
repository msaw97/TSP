# -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# Moduł zawierający implementacje grafów w postaci macierzy i listy sąsiedctwa
# oraz zdefiniowane dla nich metody.

import numpy as np
from scipy.spatial import distance

class GraphAdjacencyMatrix():
    """Reprezentacja grafu nieskierowanego w postaci macierzy sąsiedztwa."""
    def __init__(self, n, custom = None):
        if custom is None:
            self.G = np.zeros((n,n))
            self.n = n
        else:
            self.G = custom
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

    def set_G(self, array):
        self.G = array
        self.n = self.G.shape

    def add_edge(self, u, v, w):
        """Dodaje krawędź z wierzchołka u do v z wagą w."""
        if u != v:
            self.G[u][v] = w
            self.G[v][u] = w

    def remove_egde(self, u, v):
        """Usuwa krawędź z u do v"""
        self.addE(u,v, 0)

    def get_edge_weight(self, u, v):
        """Zwraca wagę krawędzi z wierzchołka u do v."""
        return self.G[u][v]

    def get_path_weight(self, path):
        """Liczy sumę wag krawędzi na scieżce."""
        pathWeight =[]

        for r in range(len(path)-1):
            pathWeight.append(self.get_edge_weight(path[r], path[r+1]))

        return sum(pathWeight)

    def calculate_distance_and_set_G(self, array_of_points):
        """Funkcja obliczająca odległość między wszystkimi punktami z tabeli
        i zapisująca je w macierzy grafu."""
        for i in range(len(array_of_points)):
            for j in range(len(array_of_points)):
                self.G[i][j] = distance.euclidean(array_of_points[i], array_of_points[j])

    def full_randomize(self, EDM, eps = 1):
        """Tworzy pełny graf n wierzchołkow z losowymi wagami."""

        def random_uniform(R):
            """Funkcja generująca liczbę z rozkładu jednostajnego w przedziale od 0 do 1.
            Następnie wygenerowana liczba jest mnożona przez 100 i zaokrąglana do R miejsc po przecinku.
            """
            return round(100 * np.random.uniform(low=0.0, high=1.0), R)

        # Jeśli spełniona jest flaga EDM, to generowany jest graf zgodny z metryką euklidesową.
        # Wszystkie krawędzie w tym grafie spełniają nierówność trójkąta.
        # Wygenerowane liczby są zaokrąglane do 2 miejsc po przecinku.
        R = 3
        if EDM: 
            self.G = np.zeros(self.G.shape)

            # Generowane są punkty na płaszczyźnie z rozkładu jednostajnego 
            array_of_points = [ (random_uniform(R), random_uniform(R)) for i in range(self.n)]
            
            # Obliczana jest odległość między wszystkimi punktami w tablicy.
            self.calculate_distance_and_set_G(array_of_points)

            # Wszystkie wagi krawędzi grafu mnożone są przez niezerowy skalar epsilon.
            self.G = self.G * eps

            return self.G

        # Dla EDM = False generowany jest graf z losowymi krawędziami.
        else:
            self.G = np.zeros(self.G.shape)
            
            for i in range(self.n):
                for j in range(self.n):
                    # Generowana jest waga danej krawędzi z rozkładu jednostajnego od 0 do 1.
                    self.G[i][j] = random_uniform(R)

            #Tworzy macierz symetryczna
            for i in range(self.n):
                for j in range(len(self.G[i][:i])):
                    self.G[i][j] = self.G[j][i]

            np.fill_diagonal(self.G, 0)

            # Wszystkie wagi krawędzi grafu mnożone są przez niezerowy skalar epsilon.
            self.G = self.G * eps

            return self.G


class Node():
    """Wierzchołek grafu."""

    def __init__(self, key, next = None):
        self.next = next
        self.key = key

    def __repr__(self):
        return str(self.key)


class Edge():
    """Krawędź grafu."""

    def __init__(self, u, v, w):
        self.u = Node(u, v)
        self.v = Node(v, u)
        self.w = w

    def __str__(self):
        return "{},{},{}".format(self.u.key,self.v.key,self.w)

    def __repr__(self):
        return str((self.u.key, self.v.key,self.w))

    def get_vertices(self):
        yield self.u.key
        yield self.v.key


class GraphAdjacencyList():
    """Reprezentacja grafu nieskierowanego w postaci listy sąsiedztwa."""

    def __init__(self, vertices):
        self.v = vertices
        self.G = [None] * self.v

    def add_edge(self, src, dest):
        """Dodaje krawędź grafu."""
        node = Node(dest)
        node.next = self.G[src]
        self.G[src] = node

        node = Node(src)
        node.next = self.G[dest]
        self.G[dest] = node

    def print_graph(self):
        """Wyświetla obecną strukure grafu jako wynik w konsoli."""
        for i in range(self.v):
            print("Lista sąsiedztwa wierzchołka {}:\nhead".format(i), end="")
            temp = self.G[i]
            while temp:
                print(" -> {}".format(temp.key), end="")
                temp = temp.next
            print(" \n")

    def size(self, node):
        """Funkcja zwracająca stopień wierzchołka."""
        size = 0
        temp = self.G[node]
        while temp:
            temp = temp.next
            size += 1
        return size

    def is_not_third(self, u, v):
        """Funkcja która sprawdza, czy dodanie krawędzi (u, v)
        nie spowoduje powstanie wierzchołka o stopniu większym niż 2.
        """

        if self.size(u) < 2 and self.size(v) < 2:
            return True

    def has_cycle(self, u, v):
        """Funkcja wykrywająca cykl w grafie, gdy dodawana jest krawędź (u,v)."""

        # Cykl może wystąpić tylko wtedy, gdy każdy z wierzchołków u i v posiada istniejącą krawędź.
        if self.G[u] == None or self.G[v] == None:
            return False

        current = self.G[u]
        visited = [u]

        while current.key != self.G[v].key:
            
            # Pętla while przechodząca po danej liście sąsiedctwa wierzchołka grafu.
            while self.G[current.key].next != None:
                if self.G[current.key].key not in visited:
                    visited.append(current.key)
                    break
                else:
                    current = self.G[current.key].next

            # Warunek istnienia cyklu.
            if current.key == self.G[v].key:
                return True

            # Warunek obsługujący przechodzenie po wierzchołkach ścieżki grafu.
            if self.G[current.key].key not in visited:
                current = self.G[current.key]
                visited.append(current.key)
            else:
                return False


    def get_path(self):
        """Funkcja przechodząca przez cały graf zwracająca ścieżkę."""

        current = self.G[0]
        visited = [0]

        for n in range(self.v):
            while current:
                if current.key not in visited:
                    visited.append(current.key)
                    break
                elif current.next != None:
                    current = current.next
                else:
                    break
            current = self.G[current.key]

        visited.append(visited[0])
        return visited


if __name__ == "__main__":
    pass