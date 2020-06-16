# -*- coding: utf-8 -*-
#Autor: Miłosz Sawicki
#Licencja: GNU GPL

import graphs
import algorithms
import time
import argparse


def CLI():
	"""Interfejs linii komend programu."""
	parser=argparse.ArgumentParser(description = "Program rozwiązujący problem komiwojażera za pomocą algorytmu dokładnego i wybranych algorymów rozwiązania przybliżonego.", prog = "TSP")
	parser.add_argument("N", type = int, help="Liczba naturalna oznaczająca ilość wierzchołków grafu.")
	parser.add_argument("-b", "--brute_force", action = "store_true", help = "Rozwiązuje TSP dokładnym algorytmem \"siłowym\".")
	parser.add_argument("-nn", "--nearest_neighbour", action = "store_true", help = "Rozwiązuje TSP algorytmem najbliższego sąsiada.")
	parser.add_argument("-se", "--smallest_edge", action = "store_true", help ="Rozwiązuje TSP algorytmem najbliższej krawędzi.")
	parser.add_argument("-rnn", "--repeated_nearest_neighbour", action = "store_true", help = "Rozwiązuje TSP powtarzalnym algorytmem najbliższej krawędzi.")
	parser.add_argument("-hk", "--held_karp", action = "store_true", help = "Rozwiązuje TSP algorytmem Helda-Karpa.")

	return vars(parser.parse_args())


args = CLI()
G = graphs.GraphAdjacencyMatrix(args["N"])
G.full_randomize()
#G.TEST()

print("Program zawierający algorytmy rozwiązujące problem komiwojażera.")
print("Macierz G na której wykonywane są obliczenia:")
print(G)

#Jeśli w argumentach nie określono algorytmów, które program ma wykonać, to wykonywane są wszystkie.
del args["N"]
if {"brute_force": False, "nearest_neighbour": False, "smallest_edge": False, "repeated_nearest_neighbour": False, "held_karp": False} == args:
	for x in args:
		args[x] = True


if args["brute_force"]:
	start_time = time.time()
	bR_BF, bR_BF_weight = algorithms.brute_force(G)
	final_time = time.time() - start_time
	print("\nAlgorytm typu brute force: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_BF, bR_BF_weight, final_time))

if args["nearest_neighbour"]:
	start_time = time.time()
	bR_NN = algorithms.nearest_neighbour(G, 0)
	final_time = time.time() - start_time
	bR_NN_weight = G.get_path_weight(bR_NN)
	print("\nAlgorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_NN, bR_NN_weight, final_time))

if args["smallest_edge"]:
	start_time =   time.time()
	bR_SE = algorithms.smallest_edge(G)
	final_time = time.time() - start_time
	bR_SE_weight = G.get_path_weight(bR_SE)
	print("\nAlgorytm najmniejszej krawędzi: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}".format(bR_SE, bR_SE_weight, final_time))


if args["repeated_nearest_neighbour"]:
	start_time =   time.time()
	bR_RNN, bR_RNN_weight = algorithms.repeated_nearest_neighbour(G)
	final_time = time.time() - start_time
	print("\nPowtarzalny algorytm najbliższego sąsiada: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_RNN, bR_RNN_weight, final_time))

if args["held_karp"]:
	start_time = time.time()
	bR_HK, bR_HK_weight = algorithms.held_karp(G)
	final_time = time.time() - start_time
	print("\nAlgorytm Helda-Karpa: {}. Łączna waga krawędzi: {}. \nCzas wykonania: {}.".format(bR_HK, bR_HK_weight, final_time))
