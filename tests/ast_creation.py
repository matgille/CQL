import ast
import sys
sys.path.append('src/')
import corpus_query_language as CQL


def test_alternative():
	print("Testing AST creation")
	query = "[lemma='esto'][lemma='ser'][]{,5}[pos='pos1']"
	query = "[lemma='lemma1'][lemma!='otro_lemma']?([lemma='esto' & pos='PP.*']|[lemma='realmente']|[lemma='ser'])[]{,5}([lemma='lemma3']|[pos='pos3'])[lemma='lemma4']?"
	CQL.utils.build_grammar(debug=True, query=query)
	exit(0)



if __name__ == '__main__':
    test_alternative()