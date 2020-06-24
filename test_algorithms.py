import unittest
import algorithms
import graphs
import numpy as np

def NN_upper_bound(n):
	return 1/2 * np.ceil(np.log(n)) + 1/2

def generate_random_graphs(n_range, total_range):
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

class TestAlgorithms(unittest.TestCase):

	def test_NN_ALG_worstcases(self):
		A_n = 4
		A = np.array([	[0, 2, 3, 7],
						[2, 0, 1, 5],
						[3, 1, 0, 4],
						[7, 5, 4, 0]])
		
		G = graphs.GraphAdjacencyMatrix(A_n, A)
		_, weight_NN = algorithms.NN_ALG(G, 1)

		self.assertEqual(weight_NN, 16)

		B = np.array([(3,3), (3.5, 2), (3.5, 1), (2, 0.5), (1, 1.5), (7	, 1.5)])

		G = graphs.GraphAdjacencyMatrix(len(B))
		G.set_G_EDM(B)
		_, weight_NN = algorithms.NN_ALG(G, 0)
		_, weight_OPT = algorithms.held_karp(G)
		print(weight_NN/weight_OPT)



if __name__ == '__main__':

	#total_range =[10, 30, 100, 250, 300, 500, 400, 200, 100, 70	, 30, 15, 10]
	#n_range = range(len(total_range))
	#A = generate_random_graphs(n_range,total_range)
	#print(len(A))
	#print(type(A[0]))

	unittest.main()

