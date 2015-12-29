from collections import namedtuple
from pos import initialPos
from either import Right, fmapEither



sourcePos, tree, remainder = 'sourcepos', 'tree', 'remainder'

ParseState = namedtuple('ParseState', [sourcePos, tree, remainder])



def initialState(sourceName, input):
    return Right(ParseState(initialPos(sourceName), None, input))




class Parser(object):

    '''below state is of type Either ParseError ParseState'''

    def __init__(self, runParser):
        self._runParser = runParser
    
    def __call__(self, state):
        return self.runParser(state)

    def runParser(self, state):
        return fmapEither(self._runParser, state)

    def __ge__(self, other):
        pass


parser = lambda x: x


def parse(sourceName, parser, input):
    return parser(initialState(sourceName, input))
