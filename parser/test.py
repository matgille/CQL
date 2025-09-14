import sys

import ply.lex as lex
import ply.yacc as yacc

# Lexer
tokens = ('LEMMA', 'EQUAL', 'VALUE', 'LSQBRACK', 'RSQBRACK')

t_EQUAL = r'='
t_LSQBRACK = r'\['
t_RSQBRACK = r'\]'

def t_LEMMA(t):
    r'lemma'
    return t

def t_VALUE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*|\'[^\']*\'|"[^"]*"'
    if t.value.startswith("'") and t.value.endswith("'"):
        t.value = t.value[1:-1]
    elif t.value.startswith('"') and t.value.endswith('"'):
        t.value = t.value[1:-1]
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Caractère inattendu: '{t.value[0]}' (ligne {t.lineno})")
    t.lexer.skip(1)

lexer = lex.lex()

# Parser
def p_bracketed_query(p):
    'query : LSQBRACK query RSQBRACK'
    p[0] = p[2]

def p_query_lemma(p):
    'query : LEMMA EQUAL VALUE'
    p[0] = ('lemma', p[3])

def p_error(p):
    if p:
        print(f"Erreur de syntaxe à '{p.value}' (ligne {p.lineno})")
    else:
        print("Erreur de syntaxe : fin de fichier inattendue")

parser = yacc.yacc(start='query')

# Test
data = "[lemma='monarchia']"
lexer.input(sys.argv[1])

ast = parser.parse(lexer=lexer)
print("AST généré :", ast)