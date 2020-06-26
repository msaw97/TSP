# -*- coding: utf-8 -*-
# Autor: Miłosz Sawicki
# Licencja: GNU GPL
# 26.06.20
# Program zawierający zestaw testów jednostkowych sprawdzających algorytmy rozwiązujące problem komiwojażera.

import unittest
import algorithms
import graphs
import numpy as np

class TestAlgorithms(unittest.TestCase):

	B = [(70, 9), (34, 8), (85, 38), (91, 94), (36, 36), (49, 56), (55, 71)]

	def test_euclidean_distance_matrix(self):
		"""Test wykonywany dla grafu, którego wierzchołki określa zbiór punktów na płaszczyźnie."""

		G = graphs.GraphAdjacencyMatrix(len(self.B))
		G.calculate_distance_and_set_G(self.B)

		# Testowany jest algorytm NN dla każdego wierzchołka początkowego:

		path, weight = algorithms.NN_ALG(G, 0)
		self.assertEqual(path, [0, 2, 5, 6, 4, 1, 3, 0])
		self.assertEqual(round(weight, 1), 347.7)

		path, weight = algorithms.NN_ALG(G, 1)
		self.assertEqual(path, [1, 4, 5, 6, 3, 2, 0, 1])
		self.assertEqual(round(weight, 1), 235.8)

		path, weight = algorithms.NN_ALG(G, 2)
		self.assertEqual(path, [2, 0, 1, 4, 5, 6, 3, 2])
		self.assertEqual(round(weight, 1), 235.8)

		path, weight = algorithms.NN_ALG(G, 3)
		self.assertEqual(path, [3, 6, 5, 4, 1, 0, 2, 3])
		self.assertEqual(round(weight, 1), 235.8)

		path, weight = algorithms.NN_ALG(G, 4)
		self.assertEqual(path, [4, 5, 6, 3, 2, 0, 1, 4])
		self.assertEqual(round(weight, 1), 235.8)

		path, weight = algorithms.NN_ALG(G, 5)
		self.assertEqual(path, [5, 6, 4, 1, 0, 2, 3, 5])
		self.assertEqual(round(weight, 1), 265.7)

		path, weight = algorithms.NN_ALG(G, 6)
		self.assertEqual(path, [6, 5, 4, 1, 0, 2, 3, 6])
		self.assertEqual(round(weight, 1), 235.8)

		# Algorytm najbliższej krawędzi:

		path, weight = algorithms.CI_ALG(G)
		self.assertEqual(path, [0, 1, 4, 5, 6, 3, 2, 0])
		self.assertEqual(round(weight, 1), 235.8)

		# Algorytmy dokładne, sprawdzana jest tylko suma wszystkich wag krawędzi cyklu:

		_, weight = algorithms.brute_force(G)
		self.assertEqual(round(weight, 1), 235.8)
		_, weight = algorithms.held_karp(G)
		self.assertEqual(round(weight, 1), 235.8)


	def test_compare_brute_force_and_held_karp(self):
		"""Test porównujący rozwiązania algorytmów dokładnych."""
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

