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
from matplotlib.ticker import MaxNLocator

np.random.seed(seed=1234)

# max_N - maksymalna liczba wierzchołków grafu - 1.
max_N = 13
# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnych z metryką euklidesową.
EDM = False
# Zmienna iterations oznacza ilość losowo generowanych grafów dla danej liczby wierzchołków N.
iterations = 10

# Lista algorytmów aproksymacyjnych problemu komiwojażera.
algorytmy_lista = [
	algorithms.NN_ALG,
	algorithms.CI_ALG,
	algorithms.RNN_ALG,
]

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_error = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_error.columns.name = 'N'

df_max_error = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_lista], index = np.arange(2, max_N))
df_max_error.columns.name = 'N'


def measure_error():
	"""Funkcja mierząca błąd względny algorytmu."""
	for alg in algorytmy_lista:
		avr_error_list = []
		max_error_list = []

		for N in np.arange(2, max_N):

			G = graphs.GraphAdjacencyMatrix(N)
			error_list = [] 

			for i in range(iterations):
				G.full_randomize(EDM)

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

			# Do wyników dodawany jest maksymalny błąd względny, który wystąpił dla danej liczby wierzchołków
			max_error_list.append(max(error_list))

		df_error[alg.__name__] = avr_error_list
		df_max_error[alg.__name__] = max_error_list
	
def plot_avr_error(df):
	"""Funkcja rysująca wykres."""

	def fit_func(x, a, b, c):
		return a*x**2 + b*x +c

	X = np.array(df.index)

	ax = plt.figure().gca()

	for Y_column in df.columns:
		Y = np.array(df[Y_column])

		params, pcov = optimize.curve_fit(fit_func, X, Y)
		ax.scatter(X, Y, label=Y_column)	
		ax.plot(X, fit_func(X, *params))

	if EDM:
		ax.set_title('Średni błąd względny algorytmów rozwiązujących TSP (EDM).')
	else:
		ax.set_title('Średni błąd względny algorytmów rozwiązujących TSP.')

	# Ustawia wartości osi X na liczby całkowite.
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))

	ax.set_xlabel("Liczba wierzchołków grafu N")  
	ax.set_ylabel('Błąd względny')
	plt.legend()
	plt.savefig("images/error_maxN({})_iter({})_EDM({}).pdf".format(max_N, iterations, EDM))
	plt.show()


if __name__ == '__main__':
	measure_error()
	
	print("\nTabela średnego błędu względnego:")
	print(df_error)
	print("Tabela maksymalnego błędu względnego:")
	print(df_max_error)
	print("EDM:", EDM)
	print("iterations:", iterations)
	plot_avr_error(df_error)