from datalang import *

import pytest

def test_empty():
    parser.parse('')
    assert parser_done.empty()

def test_spaces():
    parser.parse(' \t\r\n')
    assert parser_done.empty()

def test_numbers():
    parser.parse('-1 +2.3 -4e+5')
    ast, res = parser_done.get()
    assert ast.test() == '\n<num:-1.0>'
    assert res.test() == '\n<num:-1.0>'
    ast, res = parser_done.get()
    assert ast.test() == '\n<num:2.3>'
    assert res.test() == '\n<num:2.3>'
    ast, res = parser_done.get()
    assert ast.test() == '\n<num:-400000.0>'
    assert res.test() == '\n<num:-400000.0>'

def test_quote():
    parser.parse('`symbol')
    ast, res = parser_done.get()
    assert ast.test() == '\n<op:`>\n\t0 : <sym:symbol>'
    assert res.test() == '\n<sym:symbol>'

def test_list_empty():
    parser.parse('empty~[]')
    ast, res = parser_done.get()
    assert ast.test() == '\n<list:empty>'
    assert res.test() == '\n<list:empty>'
