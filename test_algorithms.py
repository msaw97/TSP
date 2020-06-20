import unittest
import algorithms
import graphs
import numpy as np

class TestAlgorithms(unittest.TestCase):

	def test_brute_force():
		pass
		#result = algorithms.brute_force()


def generate_random_graphs(n_range, total_range):
	"""Funkcja generująca listę losowo wygenerowanych grafów."""
	graph_list = []

	# Liczba n wierzchołków grafu jest w przedziale od 1 do 13.
	for i in n_range:
		G = graphs.GraphAdjacencyMatrix(i)

		# Ilość grafów dla danej ilości wierzchołków
		for j in total_range:
			for k in range(j):
				G.full_randomize(np.random.randint(1, 1000000))
				graph_list.append(G)

	return graph_list

if __name__ == '__main__':

	total_range =[10, 30, 100, 250, 300, 500, 400, 200, 100, 70	, 30, 15, 10]
	n_range = range(len(total_range))
	A = generate_random_graphs(n_range,total_range)
	print(len(A))
	print(type(A[0]))

	#unittest.main()