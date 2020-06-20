#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 20.06.2020
# Program przeprowadzający analize czasu wykonania zaimplementowanych algorytmów rozwiązywania problemu komiwojażera.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import algorithms
import graphs

# N - Maksymalna liczba, dla której generowane są grafu.
# Ustalana w celu stworzenia ramki danych df_time.
max_N = 100
# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnie z metryką euklidesową.
EDM = False
# Zmienna iterations oznacza ilość losowo generowanych grafów dla danej liczby wierzchołków N.
iterations = 15

# Lista zaimplenentowanych algorytmów.
algorytmy_lista = [
	algorithms.brute_force,
	algorithms.NN_ALG,
	algorithms.RNN_ALG,
	algorithms.CI_ALG,
	algorithms.held_karp,
]

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_time = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_time.columns.name = 'N'


def calulate_time(alg, EDM, m, k):
	"""Funkcja obliczająca czas wykonania algorytmu.
	m, k są granicami ilości wierzchołków grafu N.
	"""
	time_avr_list = []
	for N in np.arange(m ,k):
		G = graphs.GraphAdjacencyMatrix(N)

		# Każdy algorytm jest wykonywany 10 razy
		# Z każdą iteracją wagi krawędzi są ustawane losowo z rozkładu jednostajnego
		time_list = []
		for i in range(iterations):
			G.full_randomize(100, EDM)

			start_time = time.time()
			if alg == algorithms.NN_ALG:
				_, weight = alg(G, 1)
				print("Algorytm {}. N = {} Suma wszystkich wag krawędzi cyklu TSP: {}".format(alg.__name__, N, weight))
			else:
				_, weight = alg(G)
				print("Algorytm {}. N = {} Suma wszystkich wag krawędzi cyklu TSP: {}".format(alg.__name__, N, weight))

			time_list.append(time.time() - start_time)

		time_avr_list.append(sum(time_list) / len(time_list))

	return time_avr_list


def measure_algorithms(max_N, EDM):
	max_N = max_N -2
	for alg in algorytmy_lista:

		if alg.__name__ == "brute_force":
			time_avr_list = calulate_time(alg, EDM, 2, 9)
			time_avr_list = time_avr_list + [ np.nan for i in range(max_N -len(time_avr_list))]

		if alg.__name__ == "NN_ALG":
			time_avr_list = calulate_time(alg, EDM, 2, 100)
			time_avr_list = time_avr_list + [ np.nan for i in range(max_N -len(time_avr_list))]

		if alg.__name__ == "RNN_ALG":
			time_avr_list =	calulate_time(alg, EDM, 2, 50)
			time_avr_list = time_avr_list + [ np.nan for i in range(max_N -len(time_avr_list))]

		if alg.__name__ == "CI_ALG":
			time_avr_list = calulate_time(alg, EDM, 2, 80)
			time_avr_list = time_avr_list + [ np.nan for i in range(max_N -len(time_avr_list))]

		if alg.__name__ == "held_karp":
			time_avr_list = calulate_time(alg, EDM, 2, 14)
			time_avr_list = time_avr_list + [ np.nan for i in range(max_N -len(time_avr_list))]

		df_time[alg.__name__] = time_avr_list


def plot_time(df_time):
	"""Funkcja rysująca wykres."""
	ax = plt.gca()

	name = "Średni czas wykonania algorytmów rozwiązujących TSP."
	df_time.plot(kind='line', y='brute_force', color='red', use_index=True, ax=ax)
	df_time.plot(kind='line', y='NN_ALG', color='blue', use_index=True, ax=ax)
	df_time.plot(kind='line', y='RNN_ALG', color='green', use_index=True, ax=ax)
	df_time.plot(kind='line', y='CI_ALG', color='purple', use_index=True, ax=ax)
	df_time.plot(kind='line', y='held_karp', color='black', use_index=True, ax=ax)

	plt.show()

if __name__ == "__main__":
	measure_algorithms(max_N, EDM)
	print(df_time)	
	plot_time(df_time)
