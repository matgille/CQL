# CQL parser. Functionalities:
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

import parser as parser
import lexer as lexer
import functions as functions
import sys


class CQLEngine():
	def findall(self, corpus, query):
		query_ast = build_grammar(debug=True, query=query)
		result = parse_corpus(query_ast, corpus, debug=True, match=False)
		print(f"\n---\nResults for query {query}:")
		print(result)
		return result


	def match(self, corpus, query):
		query_ast = build_grammar(debug=True, query=query)
		result = parse_corpus(query_ast, corpus, debug=True, match=False)
		print(f"\n---\nResults for query {query}:")
		result = len(result) != 0
		print(result)
		return result


def build_grammar(debug, query):
	MyLexer = lexer.Lexer()
	MyLexer.build(query, debug=debug)
	MyParser = parser.Parser(MyLexer)
	if debug:
		print(MyParser.ast)
	return MyParser.ast


def parse_corpus(ast, corpus, debug, match=True):
	match = False
	tree_index = 0
	text_index = 0

	for item in ast:
		print(item)
	ast_length = len(ast)
	print(f"{ast_length} items to match.")

	all_spans = []
	matches = False
	first_matching_index = None
	current_initial_state = 0

	analysis_list = ['lemma', 'pos', 'morph', 'word']

	# Text-directed engine.
	while match == False:
		print("-")
		print(corpus[text_index])
		if debug:
			print(f"Text index: {text_index}")
			print(f"Tree index: {tree_index}")
			print(f"Ast length: {ast_length}")

		# On teste si on est en bout de texte.
		if len(corpus) == text_index:
			if debug:
				print("End of text. Exiting.")
			break
		if text_index + 1 == len(corpus):
			tree_index += 1
			if debug:
				print("End of text. Exiting.")
			break
		# Si on matche la longueur de notre arbre
		if tree_index == ast_length:
			all_spans.append((first_matching_index, text_index))
			first_matching_index = None
			if match is True:
				return True
			if debug:
				print(f"Appending {(first_matching_index, text_index)} to spans.")
				print(tree_index)
				print(ast_length)
			text_index += 1
			tree_index = 0
			matches = True
			# La boucle s'arrête là
		current_query = ast[tree_index]
		operator = current_query[0]
		if debug:
			print(f"Current query: {current_query}")
			print(operator)
		if operator in analysis_list:
			if debug:
				print("Operator in list of analysis")
			if functions.simple_match(current_query, corpus[text_index]):
				if debug:
					print("Found you a. Going forward on tree and text.")
					print(f"First match is {text_index}")
				if not first_matching_index:
					first_matching_index = text_index
				tree_index += 1
				text_index += 1
			else:
				tree_index = 0
				current_initial_state = current_initial_state + 1
				text_index = current_initial_state
				first_matching_index = None
				if debug:
					print(f"Nothing. Going forward on text a, at state {text_index}")
		else:
			if debug:
				print("OR, AND, DIST operator.")
				print(operator)
			if operator == "or":
				if functions.alternative_match(current_query[1:], corpus[text_index]):
					if debug:
						print("Found your alternative. Going forward on tree and text.")
						print(f"First match is {text_index}")
					if not first_matching_index:
						first_matching_index = text_index
					tree_index += 1
					text_index += 1
				else:
					if debug:
						print("Nothing. Going forward on text b.")
					tree_index = 0
					current_initial_state = current_initial_state + 1
					text_index = current_initial_state
			elif operator == "distance":
				if debug:
					print(f"Found distance operator: {current_query}")
				submatch = False
				for i in range(current_query[1][0], current_query[1][1]):
					if debug:
						print(f"\t{text_index}: Looking for {ast[tree_index + 1]} in position {text_index}")
					if len(corpus) == text_index:
						break
					if functions.simple_match(ast[tree_index + 1], corpus[text_index]):
						submatch = True
						tree_index += 2
						if debug:
							print("\tFound you b")
						text_index += 1
						break
					else:
						if debug:
							print("\tNo luck")
					text_index += 1
				if submatch is False:
					tree_index = 0
					current_initial_state = current_initial_state + 1
					text_index = current_initial_state
					first_matching_index = None
			elif operator == "and":
				all_matches = []
				for item in current_query[1:]:
					if functions.simple_match(item, corpus[text_index]):
						all_matches.append(True)
					else:
						all_matches.append(False)
				if all([item is True for item in all_matches]):
					if not first_matching_index:
						first_matching_index = text_index
					tree_index += 1
					text_index += 1
				else:
					tree_index = 0
					current_initial_state = current_initial_state + 1
					text_index = current_initial_state

	return all_spans


if __name__ == '__main__':
	query = sys.argv[1]
	corpus = functions.import_corpus("../test/test_corpus.json")
	MyEngine = CQLEngine()
	MyEngine.findall(corpus, query)
	MyEngine.match(corpus[10:30], query)