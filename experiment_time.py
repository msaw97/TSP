#  -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 20.06.2020
# Program przeprowadzający analize czasu wykonania algorytmów rozwiązujących problem komiwojażera.

import numpy as np
import pandas as pd
import time
import algorithms
import graphs
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy import optimize

np.random.seed(seed=123)

# Ustawienie zmiennej logicznej EDM na True spowoduje generowanie grafów zgodnych z metryką euklidesową.
EDM = True
# Zmienna iterations oznacza ilość losowo generowanych grafów dla danej liczby wierzchołków N.
iterations = 35


# Słownik zawierający zaimplenentowane algorytmy wraz z przypisaną do nich wartością max_N.
algorytmy_dict = {
	algorithms.brute_force : 10,
	algorithms.NN_ALG : 350,
	algorithms.RNN_ALG : 140,
	algorithms.CI_ALG : 350,
	algorithms.held_karp : 17,
}

# max_N - Maksymalna liczba, dla której generowane są grafy dla danego algorytmu.
# Jest ona ustalana w celu stworzenia ramki danych df_time.
max_N = algorytmy_dict[max(algorytmy_dict, key=algorytmy_dict.get)]

# Ramka danych, w której znajdują się wyniki z eksperymentu.
df_time = pd.DataFrame(columns = [alg.__name__ for alg in algorytmy_dict], index = np.arange(2, max_N))
df_time.columns.name = 'N'


def measure_time(max_N):
	"""Funkcja obliczająca czas wykonania algorytmu."""
	max_N = max_N - 2
	for alg, k in algorytmy_dict.items():

		avr_time_list = []
		for N in np.arange(2 , k):
			G = graphs.GraphAdjacencyMatrix(N)

			# Każdy algorytm jest wykonywany 10 razy.
			# Z każdą iteracją wagi krawędzi są ustawane losowo z rozkładu jednostajnego.
			time_list = []
			for i in range(iterations):
				G.full_randomize(EDM)

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
	ax = plt.figure().gca()

	df_time.plot(kind='line', y='brute_force', color='red', use_index=True, ax=ax)
	df_time.plot(kind='line', y='held_karp', color='black', use_index=True, ax=ax)
	df_time.plot(kind='line', y='RNN_ALG', color='orange', use_index=True, ax=ax)
	df_time.plot(kind='line', y='CI_ALG', color='green', use_index=True, ax=ax)
	df_time.plot(kind='line', y='NN_ALG', color='blue', use_index=True, ax=ax)

	# Ustawia wartości osi X na liczby całkowite.
	ax.xaxis.set_major_locator(MaxNLocator(integer=True))
	ax.set_xlabel("Liczba wierzchołków grafu N")
	ax.set_ylabel('Czas (s)')
	
	if EDM:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP (EDM).')
	else:
		ax.set_title('Średni czas wykonania algorytmów rozwiązujących TSP.')

	# Wykres zapisywany jest do folderu images, który musi znajdywać w folderze programu.
	plt.savefig("images/time_alg({}_{}_{}_{}_{})_iter({})_EDM({}).pdf".format(*algorytmy_dict.values(), iterations, EDM))
	plt.show()

if __name__ == "__main__":
	measure_time(max_N)

	print("\nTabela średnego czasu wykonania algorytmu:")
	print(df_time)	

	for x,y in algorytmy_dict.items():
		print("Maksymalne N dla {}: {}".format(x.__name__, y))
		
	print("iterations:", iterations)
	print("EDM:", EDM)
	plot_time(df_time)
