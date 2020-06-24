import unittest
import algorithms
import graphs
import numpy as np


class TestAlgorithms(unittest.TestCase):
	A = np.array([	[0, 2, 3, 7],
					[2, 0, 1, 5],
					[3, 1, 0, 4],
					[7, 5, 4, 0]])

	#B = np.array([(3,3), (3.5, 2), (3.5, 1), (2, 0.5), (1, 1.5), (7	, 1.5)])

	def test_NN_ALG_worstcases(self):

		G = graphs.GraphAdjacencyMatrix(self.A.shape[0], self.A)
		_, weight_NN = algorithms.NN_ALG(G, 1)

		self.assertEqual(weight_NN, 16)


	def test_compare_brute_force_and_held_karp(self):

		for n in range(2, 9):
			G = graphs.GraphAdjacencyMatrix(n)
			G.full_randomize

			for EDM in (False, True):
				G.full_randomize(EDM)

				weight_HK = round(algorithms.held_karp(G)[1], 3)
				weight_OPT = round(algorithms.brute_force(G)[1], 3)

				self.assertEqual(weight_OPT, weight_HK)




if __name__ == '__main__':

	unittest.main()

