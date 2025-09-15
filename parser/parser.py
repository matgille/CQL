# This is the parser
import copy
import json
import sys

import ply.lex as lex
import ply.yacc as yacc

from collections import defaultdict

def build_inverted_index(corpus):
    index = defaultdict(list)
    for token_id, token in enumerate(test_corpus):
        index[("lemma",token["lemma"])].append(token_id)
        index[("pos", token["pos"])].append(token_id)
        index[("morph", token["morph"])].append(token_id)
        index[("word", token["word"])].append(token_id)
    return index


tokens = (
    'RANGE',
    'DISTANCE',
   'OR',
   'RSQBRACK',
   'LSQBRACK',
   'EQUAL',
   'AND',
   'QUOTE',
   'LEMMA',
   'POS',
   'MORPH',
    'NUMBER',
   'WORD',
    'NOTEQUAL',
    'INTERROGATIVE',
    'PLUS',
    'VALUE',
    'ASTERISK',
)



t_OR = r"\|"
t_LSQBRACK = r"\["
t_RSQBRACK = r"\]"
t_EQUAL = r"\="
t_NOTEQUAL = r"\!="
t_AND = r"&"
t_INTERROGATIVE = r"\?"
t_PLUS = r"\+"
t_ASTERISK = r"\*"
t_ignore  = ' \t'



def t_DISTANCE(t):
    r'\[\s*\]\{[0-9]*\s*,\s*[0-9]+\}'
    range = t.value.split("]")[-1][1:-1].split(',')
    try:
        t.value = (int(range[0].strip()), int(range[1].strip()))
    except ValueError:
        t.value = (0, int(range[1].strip()))
    return t

def t_RANGE(t):
    r'\{[0-9]*\s*,\s*[0-9]+\}'
    numbers = t.value[1:-1].split(',')
    try:
        t.value = (int(numbers[0].strip()), int(numbers[1].strip()))
    except ValueError:
        t.value = (0, int(numbers[1].strip()))
    return t



def t_LEMMA(t):
    r'lemma'
    return t

def t_POS(t):
    r'pos'
    return t

def t_MORPH(t):
    r'morph'
    return t

def t_WORD(t):
    r'word'
    return t



def t_VALUE(t):
    r"'[^']+'"
    t.value = t.value[1:-1]
    return t






# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)



# Build the lexer
lexer = lex.lex(debug=False)
query = sys.argv[1]
lexer.input(query)

debug_lexer = copy.deepcopy(lexer)
while True:
    tok = debug_lexer.token()
    if not tok:
        break      # No more input
    print(tok)


#### Grammar

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
)

def p_or_queries(p):
    '''
    queries : query OR query
    | queries OR query
    '''
    if len(p) == 4:
        p[0] = [('or', p[1], p[3])]
    else:
        p[0] = [('or', p[1], p[2])]

def p_queries(p):
    '''queries : query
               | queries query
               | queries DISTANCE query'''
    if len(p) == 2:
        p[0] = [p[1]]  # Single query
        print("You're single")
    elif len(p) == 3:
        p[0] = p[1] + [p[2]]  # Append the new query to the list
    else:
        p[0] = p[1] + [('distance', p[2])] + [p[3]]



def p_distance_query(p):
    '''distance_query : query DISTANCE query'''
    print("Distance query")
    p[0] = ("distance", p[2], p[1], p[3])

def p_query(p):
    '''query : bracketed_query'''
    p[0] = p[1]


def p_bracketed_query(p):
    'bracketed_query : LSQBRACK query_content RSQBRACK'
    p[0] = p[2]


def p_ling_query(p):
    '''query_content : LEMMA EQUAL VALUE
     | POS EQUAL VALUE
     | MORPH EQUAL VALUE
     | WORD EQUAL VALUE'''
    print(f"Here: {p[1]}")
    if p[1] == "lemma":
        p[0] = ('lemma', p[3])
    elif p[1] == "pos":
        p[0] = ('pos', p[3])
    elif p[1] == "morph":
        p[0] = ('morph', p[3])
    elif p[1] == "word":
        p[0] = ('word', p[3])


def p_subquery_and_subquery(p):
    'query_content : query_content AND query_content'
    p[0] = ('and', p[1], p[3])

def p_subquery_or_subquery(p):
    'query_content : query_content OR query_content'
    p[0] = ('or', p[1], p[3])



def p_error(p):
    if p:
        print(f"Erreur de syntaxe à '{p.value}'")
    else:
        print("Erreur de syntaxe : fin de fichier inattendue")


parser = yacc.yacc(start='queries', debug=True)

ast = parser.parse(lexer=lexer, tracking=True, debug=True)

print("\nAST généré par le parser:")
print(ast)

with open("../test/test_corpus.json", "r") as f:
    test_corpus = json.load(f)[:50]

as_index = build_inverted_index(test_corpus)

match = False
tree_index = 0
text_index = 0

for item in ast:
    print(item)
ast_length = len(ast)
print(f"{ast_length} items to match.")

debug = True
all_spans = []
matches = False
first_matching_index = None

while match == False:
    print("-")
    if debug:
        print(f"Text index: {text_index}")
        print(f"Tree index: {tree_index}")
        print(f"Ast length: {ast_length}")
    if len(test_corpus) == text_index:
        break
    if text_index + 1 == len(test_corpus):
        tree_index += 1
        break
    if tree_index == ast_length:
        all_spans.append((first_matching_index, text_index))
        first_matching_index = None
        if debug:
            print(f"Appending {(first_matching_index, text_index)} to spans.")
            print(tree_index)
            print(ast_length)
        text_index += 1
        tree_index = 0
        matches = True
    current_query = ast[tree_index]
    if current_query[0] != 'distance':
        print(f"Current query: {current_query}")
        if text_index in as_index[current_query]:
            if debug:
                print("Found you a. Going forward on tree and text.")
                print(f"First match is {text_index}")
            if not first_matching_index:
                first_matching_index = text_index
            tree_index += 1
            text_index += 1
        else:
            if debug:
                print("Nothing. Going forward on text.")
            tree_index = 0
            text_index += 1
    else:
        if debug:
            print(f"Found distance operator: {current_query}")
        submatch = False
        milestone = text_index
        for i in range(current_query[1][0], current_query[1][1]):
            if debug:
                print(f"\t{text_index}: Looking for {ast[tree_index + 1]} in position {text_index}")
            if len(test_corpus) == text_index:
                break
            if text_index in as_index[ast[tree_index + 1]]:
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
            text_index = milestone + 1
            first_matching_index = None

if matches == True:
    print("Matches:")
    print(all_spans)
else:
    print("No matches")