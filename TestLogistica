import unittest
from unittest.mock import patch
import io
import sys
from HDT10 import read_graph, Graph

class TestLogistica(unittest.TestCase):
    def test_read_graph(self):
        expected_graph = Graph(4)
        expected_graph.add_edge(0, 1, 5)
        expected_graph.add_edge(0, 2, 10)
        expected_graph.add_edge(1, 2, 3)
        expected_graph.add_edge(2, 3, 1)

        expected_cities = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

        expected_edges = [(0, 1, [5, 6, 7, 8]), (0, 2, [10, 11, 12, 13]), (1, 2, [3, 4, 5, 6]), (2, 3, [1, 2, 3, 4])]

        graph, cities, edges = read_graph('test_logistica.txt')

        self.assertEqual(graph.num_vertices, expected_graph.num_vertices)
        self.assertEqual(graph.adj_matrix, expected_graph.adj_matrix)
        self.assertEqual(graph.next_matrix, expected_graph.next_matrix)
        self.assertEqual(cities, expected_cities)
        self.assertEqual(edges, expected_edges)

if __name__ == '__main__':
    unittest.main()
