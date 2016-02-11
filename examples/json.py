import sys
from jvalue import *


sys.path.append('../')


from parsefunc import *



'''
   NOTE: when defining a parser with a 'def' keyword, function MUST be
   decorated with either 'Parser' or 'syntax_tree(your_function)'.
   In this case parser's parameter is the parsing state, which will be
   implicitly passed for you when calling a top level function 'parse'.
'''


@Parser
def parseValue(s):
    return (parseNumber
          | parseAtom
          | parseString
          | parseArray
          | parseObject)(s)



@syntax_tree(Number)
def parseNumber(s):
    return integerOrDouble(s)



@syntax_tree(lambda x: Null() if x == 'null' else Bool(True if x == 'true' else False))
def parseAtom(s):
    return (string('true') | string('false') | string('null'))(s)



@syntax_tree(lambda x: String(''.join(x)))
def parseString(s):
    quote = char('"')
    return between(quote, quote, many(noneOf('"')))(s)



parseArray = syntax_tree(Array)(brackets(commaSep(parseValue)))



# example of using monadic operations ('>=' is the 'bind' operator,
# 'lift' is analogue of Haskell's 'return')
parsePair = sequence(parseString,
                     colon,
                     parseValue) >= (lambda x: lift((x[0], x[2])))


parseObject = syntax_tree(Object)(braces(commaSep(parsePair)))





if __name__ == '__main__':

    filename = 'resources/input3.txt'

    print parse(parseValue,
                file(filename).read(),
                sourceName='main.py')
