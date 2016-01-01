from state import initialParseState
from state import (
    isParseSuccess,
    isParseError,
    parseSuccessTree,
    setParseSuccessTree,
    showParseError,
    mergeErrors,
    inputConsumed
)


    



class Parser(object):

    def __init__(self, parser, arbitrary_look_ahead=False):
        self._parser               = parser
        self._arbitrary_look_ahead = arbitrary_look_ahead

    def __call__(self, state):
        return self._runParser(state)

    def _runParser(self, state):
        return self._parser(state)

    def __or__(self, other):
        @Parser
        def processor(state):
            newstate = self(state)
            if isParseSuccess(newstate):
                return newstate
            # fail if any input has been consumed
            if inputConsumed(newstate, state) and not self._arbitrary_look_ahead:
                return newstate
            newstate2 = other(state)
            return newstate2 if isParseSuccess(newstate2) else mergeErrors(newstate, newstate2)
        return processor


    
    def __and__(self, other):
        @Parser
        def processor(state):
            state = self(state)
            if isParseError(state):
                return state
            newstate = other(state)
            if isParseError(newstate):
                return newstate
            return setParseSuccessTree(newstate, [parseSuccessTree(state),
                                                  parseSuccessTree(newstate)])
        return processor


    def __ge__(self, f):
        ''' bind :: Parser a -> (a -> Parser b) -> Parser b
            f    :: a -> Parser a
        '''
        @Parser
        def processor(state):
            newstate = self(state)
            if isParseError(newstate):
                return newstate
            tree = parseSuccessTree(newstate)
            return f(tree)(newstate)
        return processor


    def __rshift__(self, other):
        "then"
        return self >= (lambda _: other)


    @staticmethod
    def pure(tree):
        "return"
        @Parser
        def processor(state):
            return setParseSuccessTree(state, tree)
        return processor


    @staticmethod
    def fmap(f, m):
        return m >= (lambda tree: pure(f(tree)))


    @staticmethod
    def tryP(parser):
        return Parser(parser._parser, arbitrary_look_ahead=True)




pure = Parser.pure
fmap = Parser.fmap
tryP = Parser.tryP
    



def syntax_tree(transform):
    '''Decorator for the user to apply a 'transform' function to the tree
    returned by the parser.'''
    def func(parser):
        @Parser
        def processor(state):
            newstate = parser(state)
            if isParseSuccess(newstate):
                tree = parseSuccessTree(newstate)
                return setParseSuccessTree(newstate, transform(tree))
            else:
                return newstate
        return processor
    return func




def parse(parser, input, sourceName=None):
    state = parser(initialParseState(sourceName, input))
    
    return parseSuccessTree(state) if isParseSuccess(state) else showParseError(state)
