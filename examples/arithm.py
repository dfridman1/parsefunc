import sys


sys.path.append('../')



from parsec import *



# parse one of passed in chars and skip trailing whitespace
op = lambda chs: oneOf(chs) >= (lambda ch: whiteSpace >> lift(ch))


plusMinus = op('+-')
multDiv   = op('*/')



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
    return reduceExprs(exprs, ops)



def reduceProduct(exprs):
    mult, div = lambda x, y: x * y, lambda x, y: x / float(y)
    ops       = {'*': mult, '/': div}
    return reduceExprs(exprs, ops)



@syntax_tree(reduceSum)
def parseExpr(s):
    return sepBy1(parseTerm, plusMinus, keep=True)(s)



product = lambda xs: reduce(lambda x, y: x * y, xs, 1)



@Parser
def parseFactor(s):
    return (parens(parseExpr) | parseNumber)(s)


@Parser
def parseNumber(s):
    '''parse a number and skip any number of trailing whitespace'''
    return (integerOrDouble >= (lambda num: whiteSpace >> lift(num)))(s)



@syntax_tree(lambda x: reduceProduct(x) if isinstance(x, list) else x)
def parseTerm(s):
    return (tryP(sepBy1(parseFactor, multDiv, keep=True)) | parseFactor)(s)





if __name__ == '__main__':

    expr = raw_input('enter expression:\n')

    print parse(parseExpr, expr, sourceName='somefile.py')
