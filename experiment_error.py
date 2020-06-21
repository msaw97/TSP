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
from scipy import optimize

np.random.seed(seed=12345)

# N - maksymalna liczba wierzchołków grafu.
max_N = 12
# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnych z metryką euklidesową.
EDM = True
# Zmienna iterations oznacza ilość losowo generowanych grafów dla danej liczby wierzchołków N.
iterations = 30

# Lista algorytmów aproksymacyjnych problemu komiwojażera.
algorytmy_lista = [
	algorithms.NN_ALG,
	algorithms.RNN_ALG,
	algorithms.CI_ALG,
]

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_error = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_error.columns.name = 'N'

def measure_error():
	"""Funkcja mierząca błąd względny algorytmu."""
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

	def fit_func(x, a, b, c):
		return a*x**2 + b*x +c

	X = np.array(df_error.index)
	for Y_column in df_error.columns:
		Y = np.array(df_error[Y_column])

		params, pcov = optimize.curve_fit(fit_func, X, Y)
		plt.scatter(X, Y, label=Y_column)	
		plt.plot(X, fit_func(X, *params))

	if EDM:
		plt.title('Średni błąd względny algorytmów rozwiązujących TSP (EDM).')
	else:
		plt.title('Średni błąd względny algorytmów rozwiązujących TSP.')

	plt.xlabel("Liczba wierzchołków grafu N")  
	plt.ylabel('Bląd względny')
	plt.legend()
	plt.show()

if __name__ == '__main__':
	measure_error()
	print(df_error)
	plot_error(df_error)