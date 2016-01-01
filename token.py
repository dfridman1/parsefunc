from char import lparen, rparen, lbrace, rbrace
from prim import pure





def enclose(open, parser, close):
    return open >> parser >= (lambda p: close >> pure(p))


def parens(parser):
    return enclose(lparen, parser, rparen)


def braces(parser):
    return enclose(lbrace, parser, rbrace)
