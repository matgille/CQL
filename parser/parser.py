# This is the parser
import copy
import sys

import ply.lex as lex
import ply.yacc as yacc

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
               | queries query'''
    if len(p) == 2:
        p[0] = [p[1]]  # Single query
        print("You're single")
    else:
        p[0] = p[1] + [p[2]]  # Append the new query to the list

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