from .primitive import *
from .number import *

from .namespace import env

import queue

########################################################## lexer

import ply.lex as lex

tokens = ['sym', 'num', 'str',
          'lq', 'rq',
          'comma', 'tild', 'tick',
          ]

t_ignore = ' \t\r'

def t_exit(t):
    r'exit\(\)'
    os._exit(0)

def t_nl(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_str(t):
    r"'.*'|\".*\""
    t.value = Str(t.value[1:-1])
    return t


t_lq = r'\['
t_rq = r'\]'

t_comma = r','
t_tild = r'~'
t_tick = r'`'

def t_num(t):
    r'[+\-]?[0-9]+(\.[0-9]+)?([eE][+\-]?[0-9]+)?'
    t.value = Num(t.value)
    return t

def t_sym(t):
    r'[^ \t\r\n\(\)\[\]\{\}\,\~\`]+'
    t.value = Sym(t.value)
    return t

def t_ANY_error(t): raise SyntaxError(t)


lexer = lex.lex()


########################################################## parser

import ply.yacc as yacc

import traceback

import queue
parser_queue = queue.Queue()

################################## REPL

def p_REPL_none(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    ast = p[2]                        # parsed AST
    global env
    try:
        result = p[2].eval(env)       # evaluated AST
    except Exception as err:
        result = None
        traceback.print_exc()
    parser_queue.put([ast, result])

############################################ literals

## symbol
def p_ex_sym(p):
    ' ex : sym '
    p[0] = p[1]

## number
def p_ex_num(p):
    ' ex : num '
    p[0] = p[1]

## string
def p_ex_str(p):
    ' ex : str '
    p[0] = p[1]

############################################ operators

## `(1+2) --> ast: op:+ // num:1 // num:2
def p_ex_quote(p):
    ' ex : tick ex '
    p[0] = Op(p[1]) // p[2]

## name~[]
def p_ex_nameit(p):
    ' ex : sym tild ex '
    p[0] = p[3]
    p[3].value = p[1].value

############################################### parens

def p_ex_list(p):
    ' ex : lq seq rq '
    p[0] = p[2]

def p_seq_none(p):
    ' seq : '
    p[0] = List()
def p_list_spaced(p):
    ' seq : seq ex '
    p[0] = p[1] // p[2]
def p_list_comma(p):
    ' seq : seq comma ex '
    p[0] = p[1] // p[3]


def p_error(p): raise SyntaxError(p)


parser = yacc.yacc(debug=False, write_tables=False)
