#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 20.06.2020
# Program przeprowadzający analize czasu wykonania algorytmów rozwiązujących problem komiwojażera.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import algorithms
import graphs

np.random.seed(seed=12345)

# max_N - Maksymalna liczba, dla której generowane są grafy,
# ustalana w celu stworzenia ramki danych df_time.
max_N = 100
# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnych z metryką euklidesową.
EDM = False
# Zmienna iterations oznacza ilość losowo generowanych grafów dla danej liczby wierzchołków N.
iterations = 20


# Słownik zawierający zaimplenentowane algorytmy wraz z przypisaną do nich wartością max_N.
algorytmy_lista = {
	algorithms.brute_force : 9,
	algorithms.NN_ALG : 100,
	algorithms.RNN_ALG : 60,
	algorithms.CI_ALG : 80,
	algorithms.held_karp : 15,
}

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_time = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_time.columns.name = 'N'


def measure_time(max_N):
	"""Funkcja obliczająca czas wykonania algorytmu."""
	max_N = max_N - 2
	for alg, k in algorytmy_lista.items():

		avr_time_list = []
		for N in np.arange(2 , max_N):
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

		avr_time_list = avr_time_list + [ np.nan for i in range(max_N -len(avr_time_list))]

		df_time[alg.__name__] = avr_time_list


def plot_time(df_time):
	"""Funkcja rysująca wykres."""
	ax = plt.gca()

	df_time.plot(kind='line', y='brute_force', color='red', use_index=True, ax=ax)
	df_time.plot(kind='line', y='NN_ALG', color='blue', use_index=True, ax=ax)
	df_time.plot(kind='line', y='RNN_ALG', color='orange', use_index=True, ax=ax)
	df_time.plot(kind='line', y='CI_ALG', color='green', use_index=True, ax=ax)
	df_time.plot(kind='line', y='held_karp', color='black', use_index=True, ax=ax)
	ax.set_xlabel("Liczba wierzchołków grafu N")
	ax.set_ylabel('Czas (s)')
	if EDM:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP (EDM).')
	else:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP.')

	plt.show()

if __name__ == "__main__":
	measure_time(max_N)
	print(df_time)	
	plot_time(df_time)
