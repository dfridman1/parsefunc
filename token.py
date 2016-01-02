from char import lparen, rparen, lbrace, rbrace
from combinators import between




def parens(parser):
    return between(lparen, rparen, parser)


def braces(parser):
    return between(lbrace, rbrace, parser)
