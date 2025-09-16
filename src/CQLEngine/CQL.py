# Python package project: CQL (Corpus Query Language) parser:
# - parsing of any kind of annotation: word, lemma, pos, morph
# - combination of annotations: [lemma='rey' & pos='NCMP000']
# - one or zero annotations [lemma='rey']?. For one ore more, see the distance operator
# - distance [lemma='rey'][]{,5}[lemma='santo']
# - any regex in the annotation value [lemma='reye?s?']
# - alternatives: [lemma='rey']|[lemma='príncipe'][]{,5}[lemma='santo']
import json

# Takes a list of dicts with the annotations as input. Returns:
# - a list of spans (search_all function)
# - a boolean (match function)

import src.CQLEngine.parser as parser
import src.CQLEngine.lexer as lexer
import src.CQLEngine.functions as functions
import src.CQLEngine.engine as engine
import sys


class CQLEngine():
	def findall(self, corpus:list[dict], query:str, debug) -> list[tuple[int, int]]:
		"""
			This function checks if a query matches some text, and returns the start and end span.
			:param query: a CQL query
			:param corpus: the annotated text as a list of dictionnaries containing the annotations (lemma, pos, morph, word)
			:return: a list of tuples with the start and end position.
			"""
		query_ast = build_grammar(debug=debug, query=query)
		result = engine.parse_corpus(query_ast, corpus, debug=debug, match=False)
		print(f"\n---\nResults for query {query}:")
		print(f"Ast: {query_ast}")
		print(f"Spans: {result}")
		return result


	def match(self, corpus:list[dict], query:str, debug:bool) -> bool:
		"""
		This function checks whether a query matches some text, and returns True or False
		:param query: a CQL query
		:param corpus: the annotated text as a list of dictionnaries containing the annotations (lemma, pos, morph, word)
		:return: a boolean
		"""
		query_ast = build_grammar(debug=debug, query=query)
		result = engine.parse_corpus(query_ast, corpus, debug=debug, match=False)
		print(f"\n---\nResults for query {query}:")
		result = len(result) != 0
		print(result)
		return result


def build_grammar(debug, query):
	MyLexer = lexer.Lexer()
	MyLexer.build(query, debug=debug)
	MyParser = parser.Parser(MyLexer, debug=debug)
	if debug:
		print(MyParser.ast)
	return MyParser.ast





if __name__ == '__main__':
	query = sys.argv[1]
	corpus = functions.import_corpus("test/test_corpus.json")
	MyEngine = CQLEngine()
	MyEngine.findall(corpus, query)
	# MyEngine.match(corpus, query)