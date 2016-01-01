from char import lparen, rparen, lbrace, rbrace
from combinators import sequence
from state import isParseError, parseSuccessTree, setParseSuccessTree
from prim import syntax_tree





def enclose(open, parser, close):
    return syntax_tree(lambda x: x[1])(open & parser & close)



def parens(parser):
    return enclose(lparen, parser, rparen)


def braces(parser):
    return enclose(lbrace, parser, rbrace)
