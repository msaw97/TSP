#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 20.06.2020
# Program przeprowadzający analize błędu algorytmów aproksymacyjnych problemu komiwojażera.

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import algorithms
import graphs

EDM = False
iterations = 20
max_N = 16

# Lista algorytmów aproksymacyjnych.
algorytmy_lista = [
	algorithms.NN_ALG,
	algorithms.RNN_ALG,
	algorithms.CI_ALG,
]

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_error = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_error.columns.name = 'N'

opt_weight_list = []

for alg in algorytmy_lista:
	avr_error_list = []

	for N in np.arange(2, max_N):

		G = graphs.GraphAdjacencyMatrix(N)
		error_list = [] 

		for i in range(iterations):
			G.full_randomize(100, EDM)

			# Algorytm Helda-Karpa znajduje opymalny cykl TSP.
			_, opt_weight = algorithms.held_karp(G)

			# Obliczany jest bląd względny rozwiązania przybliżonego.
			if alg == algorithms.NN_ALG:
				_, weight = alg(G, 0)
				error = weight/opt_weight
				error_list.append(error)
				print("Algorytm {}. N = {} Błąd względny algorytmu: {}".format(alg.__name__, N, error))
			else:
				_, weight = alg(G)
				error = weight/opt_weight
				error_list.append(error)
				print("Algorytm {}. N = {} Błąd względny algorytmu: {}".format(alg.__name__, N, error))

		# Obliczany jest średni błąd względny dla danej liczby wierzchołków N.
		avr_error_list.append(sum(error_list) / len(error_list))

	df_error[alg.__name__] = avr_error_list
	
def plot_error(df_error):
	"""Funkcja rysująca wykres."""
	ax = plt.gca()

	df_error.plot(kind='line', y='NN_ALG', color='blue', use_index=True, ax=ax)
	df_error.plot(kind='line', y='RNN_ALG', color='green', use_index=True, ax=ax)
	df_error.plot(kind='line', y='CI_ALG', color='purple', use_index=True, ax=ax)
	ax.set_xlabel("Liczba wierzchołków grafu N")
	ax.set_ylabel('Czas (s)')
	if EDM:
		ax.set_title('Średni błąd względny algorytmów rozwiązujących TSP (EDM).')
	else:
		ax.set_title('Średni błąd względny algorytmów rozwiązujących TSP.')

	plt.show()


if __name__ == '__main__':
	print(df_error)
	plot_error(df_error)