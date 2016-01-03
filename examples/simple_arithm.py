import sys

sys.path.append('..')


from parsec import *


op = lambda ch: char(ch) >= (lambda x: whiteSpace >> lift(x))

plus = op('+')
mult = op('*')


@syntax_tree(sum)
def parseExpr(s):
    return sepBy(parseTerm, plus)(s)


@Parser
def parseFactor(s):
    return (parens(parseExpr) | parseNatural)(s)


@Parser
def parseNatural(s):
    return (natural >= (lambda num: many(space) >> lift(num)))(s)


product = lambda xs: reduce(lambda x, y: x * y, xs, 1)


@syntax_tree(lambda x: product(x) if isinstance(x, list) else x)
def parseTerm(s):
    return (tryP(sepBy(parseFactor, mult)) | parseFactor)(s)




if __name__ == '__main__':
    
    expr = raw_input('enter expression:\n')

    print parse(parseExpr, expr, sourceName='somefile.py')
