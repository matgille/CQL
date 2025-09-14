import re
import parser.parser as parser
# Python package project: CQL (Corpus Query Language) parser.


def parse(query:str) -> None:
	"""
	The CQL parser
	:param query: a CQL query
	:return: To be defined
	"""
	return


def findall(query:str, text:list[dict]) -> (int, int):
	"""
	This function checks if a query matches some text, and returns the start and end span.
	:param query: a CQL query
	:param text: the annotated text as a list of dictionnaries containing the annotations (lemma, pos, morph, word)
	:return: a tuple with the start and end position.
	"""
	return


def match(query:str, text: list[dict]) -> bool:
	"""
	This function checks whether a query matches some text, and returns True or False
	:param query: a CQL query
	:param text: the annotated text as a list of dictionnaries containing the annotations (lemma, pos, morph, word)
	:return: a boolean
	"""
	return

def main():
	print("Work in progress")

if __name__ == '__main__':
    main()