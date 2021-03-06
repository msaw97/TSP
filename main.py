#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 26.06.20
# Główny blok programu. 
#
# W celu uruchomienia programu należy określić liczbę wierzchołków grafu N
# oraz wybrać dodatkowe funkcjonalności. 
# Spis argumentów programu dostępny jest po wywołaniu: python main.py -h
# Dodatkowe argumenty należy poprzedzić myślnikiem.
#
# Przykład uruchomienia programu w celu rozwiązania TSP dla grafu o 8 wierzchołkach, 
# o losowych krawędziach spełniających nierówność trojkąta,
# algorytmem najbliższego sąsiada i algorytmem Helda-Karpa:
# python main.py 8 -nn -hk -EDM

import graphs
import algorithms
import time
import argparse


def CLI():
	"""Interfejs linii komend programu."""
	parser=argparse.ArgumentParser(description = "Program rozwiązujący problem komiwojażera za pomocą algorytmu dokładnego " +
	"i wybranych algorymów rozwiązania przybliżonego. " +
	"Autor: Miłosz Sawicki " +
	"Przykładowe wywołanie w konsoli: python main.py 8 -b -ci -hk", prog = "TSP")
	parser.add_argument("N", type = int, help="Liczba naturalna oznaczająca ilość wierzchołków grafu.")
	parser.add_argument("-b", "--brute_force", action = "store_true", help = "Rozwiązuje TSP dokładnym algorytmem \"siłowym\".")
	parser.add_argument("-nn", "--NN_ALG", action = "store_true", help = "Rozwiązuje TSP algorytmem najbliższego sąsiada.")
	parser.add_argument("-ci", "--CI_ALG", action = "store_true", help ="Rozwiązuje TSP algorytmem najbliższej krawędzi.")
	parser.add_argument("-rnn", "--RNN_ALG", action = "store_true", help = "Rozwiązuje TSP powtarzalnym algorytmem najbliższej krawędzi.")
	parser.add_argument("-hk", "--held_karp", action = "store_true", help = "Rozwiązuje TSP dokładnym algorytmem Helda-Karpa.")
	parser.add_argument("-eps", type = float, help = "Określa liczbę zmiennoprzecinkową, przez którą przemnożone będą wszystkie wagi krawędzi grafu.")
	parser.add_argument("-EDM", help = "Graf zgodny z metryką euklidesową.",action = "store_true")

	return vars(parser.parse_args())


args = CLI()
G = graphs.GraphAdjacencyMatrix(args["N"])

# Funkcja full_randomize pozwala,czy macierz sąsiadctwa grafu będzie posiadała metrykę euklidesową oraz
# wybrać niezerowy skalar, przez który będą przemnożone wszystkie wagi krawędzi grafu.
if args["eps"] and args["eps"] > 0:
	G.full_randomize(args["EDM"], args["eps"])
else:
	# domyślna wartość epsilon - 100
	G.full_randomize(args["EDM"])


print("Program zawierający algorytmy rozwiązujące problem komiwojażera.")
#print("Macierz G na której wykonywane są obliczenia: \n{}".format(G))

# Jeśli w argumentach nie określono algorytmów, które program ma wykonać, to wykonywane są wszystkie.
del args["N"]
del args["eps"]
del args["EDM"]
if {"brute_force": False, "NN_ALG": False, "CI_ALG": False, "RNN_ALG": False, "held_karp": False} == args:
	for x in args:
		args[x] = True

if args["brute_force"]:
	start_time = time.time()
	bR_BF, bR_BF_weight = algorithms.brute_force(G)
	final_time = time.time() - start_time
	print("\nAlgorytm typu brute force. Cykl TSP: {}. Suma wag krawędzi cyklu: {} \nCzas wykonania: {}.".format(bR_BF, bR_BF_weight, final_time))

if args["NN_ALG"]:
	start_time = time.time()
	bR_NN, bR_NN_weight = algorithms.NN_ALG(G, 0)
	final_time = time.time() - start_time
	print("\nAlgorytm najbliższego sąsiada. Cykl TSP: {}. Suma wag krawędzi cyklu: {} \nCzas wykonania: {}.".format(bR_NN, bR_NN_weight, final_time))

if args["RNN_ALG"]:
	start_time = time.time()
	bR_RNN, bR_RNN_weight = algorithms.RNN_ALG(G)
	final_time = time.time() - start_time
	print("\nPowtarzalny algorytm najbliższego sąsiada. Cykl TSP: {}. Suma wag krawędzi cyklu: {} \nCzas wykonania: {}.".format(bR_RNN, bR_RNN_weight, final_time))

if args["CI_ALG"]:
	start_time = time.time()
	bR_CI, bR_CI_weight = algorithms.CI_ALG(G)
	final_time = time.time() - start_time
	print("\nAlgorytm najmniejszej krawędzi. Cykl TSP: {}. Suma wag krawędzi cyklu: {} \nCzas wykonania: {}".format(bR_CI, bR_CI_weight, final_time))


if args["held_karp"]:
	start_time = time.time()
	bR_HK, bR_HK_weight = algorithms.held_karp(G)
	final_time = time.time() - start_time
	print("\nAlgorytm Helda-Karpa. Cykl TSP: {}. Suma wag krawędzi cyklu: {} \nCzas wykonania: {}".format(bR_HK, bR_HK_weight, final_time))
