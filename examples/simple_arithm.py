import sys

sys.path.append('..')


from pyparsec import *


plus, mult = char('+'), char('*')


@syntax_tree(sum)
def parseExpr(s):
    return sepBy(parseTerm, plus)(s)


product = lambda xs: reduce(lambda x, y: x * y, xs, 1)


@syntax_tree(product)
def parseTerm(s):
    return sepBy(parseFactor, mult)(s)


@Parser
def parseFactor(s):
    return between(whiteSpace, whiteSpace, parens(parseExpr) | integer)(s)




if __name__ == '__main__':

    expr = raw_input('enter expression:\n')

    print parse(parseExpr, expr, sourceName='simple_arithm.py')
