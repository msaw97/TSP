#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 20.06.2020
# Program przeprowadzający analize czasu wykonania algorytmów rozwiązujących problemu komiwojażera.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import algorithms
import graphs
#from numba import jit, cuda 


# N - Maksymalna liczba, dla której generowane są grafu.
# Ustalana w celu stworzenia ramki danych df_time.
max_N = 100
# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnych z metryką euklidesową.
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

def calulate_time(alg, m, k):
	"""Funkcja obliczająca czas wykonania algorytmu.
	m, k są granicami przedziału, w którym zawiera się liczba wierzchołków grafu N.
	"""
	avr_time_list = []
	for N in np.arange(m ,k):
		G = graphs.GraphAdjacencyMatrix(N)

		# Każdy algorytm jest wykonywany 10 razy.
		# Z każdą iteracją wagi krawędzi są ustawane losowo z rozkładu jednostajnego.
		time_list = []
		for i in range(iterations):
			G.full_randomize(100, EDM)

			# Obliczany jest czas wykonania algorytmów.
			start_time = time.time()
			if alg == algorithms.NN_ALG:
				_, weight = alg(G, 0)
				print("Algorytm {}. N = {} Suma wszystkich wag krawędzi cyklu TSP: {}".format(alg.__name__, N, weight))
			else:
				_, weight = alg(G)
				print("Algorytm {}. N = {} Suma wszystkich wag krawędzi cyklu TSP: {}".format(alg.__name__, N, weight))

			time_list.append(time.time() - start_time)

		# Obliczany jest średni czas wykonania algorytmów.
		avr_time_list.append(sum(time_list) / len(time_list))

	return avr_time_list


def measure_algorithms(max_N):
	max_N = max_N -2
	for alg in algorytmy_lista:

		if alg.__name__ == "brute_force":
			avr_time_list = calulate_time(alg, 2, 9)
			avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		if alg.__name__ == "NN_ALG":
			avr_time_list = calulate_time(alg, 2, 100)
			avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		if alg.__name__ == "RNN_ALG":
			avr_time_list =	calulate_time(alg, 2, 50)
			avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		if alg.__name__ == "CI_ALG":
			avr_time_list = calulate_time(alg, 2, 80)
			avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		if alg.__name__ == "held_karp":
			avr_time_list = calulate_time(alg, 2, 14)
			avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		df_time[alg.__name__] = avr_time_list


def plot_time(df_time):
	"""Funkcja rysująca wykres."""
	ax = plt.gca()

	df_time.plot(kind='line', y='brute_force', color='red', use_index=True, ax=ax)
	df_time.plot(kind='line', y='NN_ALG', color='blue', use_index=True, ax=ax)
	df_time.plot(kind='line', y='RNN_ALG', color='green', use_index=True, ax=ax)
	df_time.plot(kind='line', y='CI_ALG', color='purple', use_index=True, ax=ax)
	df_time.plot(kind='line', y='held_karp', color='black', use_index=True, ax=ax)
	ax.set_xlabel("Liczba wierzchołków grafu N")
	ax.set_ylabel('Czas (s)')
	if EDM:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP (EDM).')
	else:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP.')

	plt.show()

if __name__ == "__main__":
	measure_algorithms(max_N)
	print(df_time)	
	plot_time(df_time)
