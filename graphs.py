# -*- coding: utf-8 -*-

import numpy as np


class GraphAdjacencyMatrix():
    """Reprezentacja grafu nieskierowanego w postaci macierzy sąsiedztwa."""
    def __init__(self, n):
        self.G = np.zeros((n,n))
        self.n = n

    def TEST(self):
        self.G = np.array ([[0,91,56,99,70,87,70],
                            [91,0,38,83,70,47,3],
                            [56,38 ,0 ,51,8,95,16],
                            [99,83,51,0,24,55,73],
                            [70,70 ,8,24,0,50,19],
                            [87,47,95,55 ,50,0,15],
                            [70,3,16,73,19,15,0],])

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
        """Dodaje krawędź z wierzchołka u do v z wagą w."""
        if u != v:
            self.G[u][v] = w
            self.G[v][u] = w

    def removeE(self, u, v):
        """Usuwa krawędź z u do v"""
        self.addE(u,v, 0)

    def getWeight(self, u, v):
        """Zwraca wagę krawędzi z wierzchołka u do v."""
        return self.G[u,v]

    def getRouteWeight(self, route):
        """Liczy sumę wag krawędzi na scieżce."""
        routeWeight =[]

        for r in range(len(route)-1):
            routeWeight.append(self.getWeight(route[r], route[r+1]))

        return sum(routeWeight)

    def full_randomize(self):
        """Tworzy pełny graf n wierzchołkow z losowymi wagami."""
        self.G = np.random.randint(1,100, self.G.shape)

        #tworzy macierz symetryczna
        for i in range(self.n):
            for j in range(len(self.G[i][:i])):
                self.G[i][j] = self.G[j][i]

        np.fill_diagonal(self.G, 0)
        return self.G


class GraphAdjacencyList():
    """Reprezentacja grafu nieskierowanego w postaci listy sąsiedztwa."""

    def __init__(self, vertices):
        self.v = vertices
        self.G = [None] * self.v

    def add_edge(self, src, dest):
        node = Node(dest)
        node.next = self.G[src]
        self.G[src] = node

        node = Node(src)
        node.next = self.G[dest]
        self.G[dest] = node

    def print_graph(self):
        for i in range(self.v):
            print("Lista sąsiedztwa wierzchołka {}:\nhead".format(i), end="")
            temp = self.G[i]
            while temp:
                print(" -> {}".format(temp.key), end="")
                temp = temp.next
            print(" \n")

    def size(self, node):
        """Funkcja zwracająca ilość krawędzi wychodzących z wierzchołka."""
        size = 0
        temp = self.G[node]
        while temp:
            temp = temp.next
            size += 1
        return size

    def is_not_third(self, u, v):
        """Funkcja która sprawdza, czy dodanie krawędzi spowoduje powstanie wierzchołka,
        z którego wychodzą trzy krawędzie."""
        if self.size(u) < 2 and self.size(v) < 2:
            return True

    def has_cycle(self, u, v):
        """Funkcja wykrywająca cykl w grafie, gdy dodawana jest krawędź (u,v)."""

        #cykl może wystąpić tylko wtedy, gdy każdy z wierzchołków u i v posiada istniejącą krawędź
        if self.G[u] == None or self.G[v] == None:
            return False

        current = self.G[u]
        visited = [u]


        while current.key != self.G[v].key:

            #pętla while przechodząca po danej liście sąsiedctwa wierzchołka grafu
            while self.G[current.key].next != None:
                if self.G[current.key].key not in visited:
                    visited.append(current.key)
                    break
                else:
                    current = self.G[current.key].next

            #warunek istnienia cyklu
            if current.key == self.G[v].key:
                return True

            #warunek obsługujący przechodzenie po wierzchołkach ścieżki grafu
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


if __name__ == "__main__":
    G = GraphAdjacencyMatrix(7)
    G.addE(0,2,6)
    G.addE(1,4,5)
    G.addE(3,3,4)
    G.removeE(1,4)
    print(G)
    print(G.full_randomize())

    lst = []
    e = Edge(1,2,20)
    lst.append(e)
    print(lst)

    node1 = Node(1)
    node2 = Node(2)
    edge1 = Edge(node1,node2, 10)