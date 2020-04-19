# -*- coding: utf-8 -*-

import graphs
import algorithms
import time


G = graphs.GraphAdjacencyMatrix(7)
G.full_randomize()
#G.TEST()

print("Najkrótsza scieżka problemu TSP.")
print(G)

start_time = time.time()
bR_BF, bRW_BF = algorithms.brute_force(G)
final_time = time.time() - start_time
print("\nAlgorytm typu brute force: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_BF, bRW_BF, final_time))

start_time = time.time()
bR_NN = algorithms.nearest_neighbour(G, 0)
final_time = time.time() - start_time
bRW_NN = G.getRouteWeight(bR_NN)
print("\nAlgorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_NN, bRW_NN, final_time))

start_time =   time.time()
bR_SE = algorithms.smallest_edge(G)
final_time = time.time() - start_time
bRW_SE = G.getRouteWeight(bR_SE)
print("\nAlgorytm najmniejszej krawędzi: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}".format(bR_SE, bRW_SE, final_time))

start_time =   time.time()
bR_RNN, bRW_RNN = algorithms.RNN(G)
final_time = time.time() - start_time
print("\nPowtarzalny algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_RNN, bRW_RNN, final_time))
