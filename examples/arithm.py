import sys


sys.path.append('..')


from pyparsec import *


plusMinus = oneOf('+-')
multDiv   = oneOf('*/')



def reduceExprs(exprs, ops, default=0):
    '''ops is a dict, where keys are binary ops representations (ie, '+', '-')
       and values are the corresponding binary functions.
       exprs = [num1, op1, num2, op2, num3, ..., numk]
    '''
    res = exprs[0] if exprs != [] else default
    for i in xrange(2, len(exprs), 2):
        num, op = exprs[i], exprs[i-1]
        res = ops[op](res, num)   # apply a binary function
    return res



def reduceSum(exprs):
    add, sub = lambda x, y: x + y, lambda x, y: x - y
    ops      = {'+': add, '-': sub}
    return reduceExprs(exprs, ops, default=0)



def reduceProduct(exprs):
    mult, div = lambda x, y: x * y, lambda x, y: x / float(y)
    ops       = {'*': mult, '/': div}
    return reduceExprs(exprs, ops, default=1)



@syntax_tree(reduceSum)
def parseExpr(s):
    return sepBy(parseTerm, plusMinus, keep=True)(s)


@syntax_tree(reduceProduct)
def parseTerm(s):
    return sepBy(parseFactor, multDiv, keep=True)(s)


@Parser
def parseFactor(s):
    return between(whiteSpace,
                   whiteSpace,
                   parens(parseExpr) | integerOrDouble)(s)



if __name__ == '__main__':

    expr = raw_input('enter expression:\n')

    print parse(parseExpr, expr, 'arithm.py')
