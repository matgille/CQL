import ast
import sys
sys.path.append('src/')
import corpus_query_language as CQL
import unittest

def import_test_queries(path):
	with open(path, "r") as f:
		list_of_queries = f.read().splitlines()
	return [line.split("\t") for line in list_of_queries]

def import_match_queries(path):
	with open(path, "r") as f:
		list_of_queries = f.read().splitlines()
	as_splits = [line.split("\t") for line in list_of_queries]
	return [(ast.literal_eval(nodes), query, GT) for nodes, query, GT in as_splits]

class TestAstBuilding(unittest.TestCase):
	def test_first_test(self):
		print("Testing AST creation")
		queries = ["[lemma='esto'][lemma='ser'][]{,5}[lemma='algo']",
				   "[lemma='esto'][lemma='ser'][]{,5}([lemma='lemma1']|[pos='pos1'])"]
		gts = [[('lemma', '=', 'esto'), ('lemma', '=', 'ser'), ('distance', (0, 5)), ('lemma', '=', 'algo')],
			   [('lemma', '=', 'esto'), ('lemma', '=', 'ser'), ('distance', (0, 5)), ('distance', ('lemma', '=', 'algo'), ('pos', '=', 'pos1'))]]
		queries_and_gts = zip(queries, gts)
		self.MyEngine = CQL.core.CQLEngine()
		for query, gt in queries_and_gts:
			query_ast = CQL.utils.build_grammar(debug=False, query=query)
			with self.subTest(query=query, GT=gt):
				self.assertEqual(query_ast, gt)

class TestFunctions(unittest.TestCase):
	def test_simple_match(self):
		print("Testing simple match")
		query = ("lemma", "=", "asno")
		test_token = {"lemma": "asno",
					  "pos": "NCMS000",
					  "morph": None,
					  "word": "asnos"}
		self.assertEqual(CQL.utils.simple_match(query, test_token), True, "Something is wrong "
																		  "with function `test_simple_match`")
		print("Test passed.")

class TestQueries(unittest.TestCase):
	def test_findall_queries(self):
		print("\n\n-----\nTesting findall queries")
		self.corpus = CQL.utils.import_corpus("tests/test_data/test_corpus.json")
		self.queries = import_test_queries("tests/queries_findall.txt")
		self.MyEngine = CQL.core.CQLEngine()
		for query, GT in self.queries:
			GT = ast.literal_eval(GT)
			with self.subTest(query=query, GT=GT):
				self.assertEqual(self.MyEngine.findall(self.corpus, query, debug=False), GT, "Error with findall function")
		print("Test passed.")

	def test_match_queries(self):
		print("\n\n-----\nTesting match queries")
		self.queries = import_match_queries("tests/queries_match.txt")
		self.MyEngine = CQL.core.CQLEngine()
		for idx, (nodes, query, GT) in enumerate(self.queries):
			with self.subTest(query=query, GT=GT):
				GT = True if GT == "True" else False
				match = self.MyEngine.match(nodes, query, debug=False)
				self.assertEqual(match, GT,
								 msg=f"\nTest {idx + 1} failed.\n"
									 f"Query: {query}\n"
									 f"Nodes: {nodes}\n"
									 f"Match should be {GT}, is {match}")


if __name__ == '__main__':
	unittest.main()