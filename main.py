# -*- coding: utf-8 -*-

import graphs
import algorithms
import time


G = graphs.GraphAdjacencyMatrix(4)
G.full_randomize()
G.TEST()

print("Najkrótsza scieżka problemu TSP.")
print(G)

start_time = time.time()
bR_BF, bR_BF_weight = algorithms.brute_force(G)
final_time = time.time() - start_time
print("\nAlgorytm typu brute force: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_BF, bR_BF_weight, final_time))

start_time = time.time()
bR_NN = algorithms.nearest_neighbour(G, 0)
final_time = time.time() - start_time
bR_NN_weight = G.get_path_weight(bR_NN)
print("\nAlgorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_NN, bR_NN_weight, final_time))

start_time =   time.time()
bR_SE = algorithms.smallest_edge(G)
final_time = time.time() - start_time
bR_SE_weight = G.get_path_weight(bR_SE)
print("\nAlgorytm najmniejszej krawędzi: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}".format(bR_SE, bR_SE_weight, final_time))

start_time =   time.time()
bR_RNN, bR_RNN_weight = algorithms.repeated_nearest_neighbour(G)
final_time = time.time() - start_time
print("\nPowtarzalny algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_RNN, bR_RNN_weight, final_time))

start_time = time.time()
bR_HK = algorithms.held_karp(G)
final_time = time.time() - start_time
bR_HK_weight = G.get_path_weight(bR_HK)
print("\nAlgorytm Helda-Karpa: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_HK, bR_HK_weight, final_time))
