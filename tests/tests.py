import ast
import json
import unittest

import src.CQLEngine.CQL as CQLEngine
import src.CQLEngine.functions as functions

import unittest

def import_test_queries(path):
	with open(path, "r") as f:
		list_of_queries = f.read().splitlines()
	return [line.split("\t") for line in list_of_queries]

class TestStringMethods(unittest.TestCase):

	def test_findall_queries(self):
		self.corpus = functions.import_corpus("test_data/test_corpus.json")
		self.queries = import_test_queries("tests/queries_findall.txt")
		self.MyEngine = CQLEngine.CQLEngine()
		for query, GT in self.queries:
			GT = ast.literal_eval(GT)
			with self.subTest(query=query, GT=GT):
				self.assertEqual(self.MyEngine.findall(self.corpus, query, debug=False), GT)


	def test_match_queries(self):
		self.corpus = functions.import_corpus("test_data/test_corpus.json")
		self.queries = import_test_queries("tests/queries_match.txt")
		self.MyEngine = CQLEngine.CQLEngine()
		for query, GT in self.queries:
			with self.subTest(query=query, GT=GT):
				GT = True if GT == "True" else False
				self.assertEqual(self.MyEngine.match(self.corpus, query, debug=False), GT)


if __name__ == '__main__':
	unittest.main()