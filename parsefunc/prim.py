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
        '''First runs parser 'self'. If it succeeds, returns value returned by it.
        Otherwise, runs parser 'other', returning the corresponding value.
        If both fail, returns 'the farthest into the input' error.
        VERY IMPORTANT: if parser 'self' fails, but consumes input, then
        parser 'other' is not tried - error from parser 'self' is returned.
        '''

        @Parser
        def processor(state):
            newstate = self(state)
            if isParseSuccess(newstate):
                return newstate
            # fail if any input has been consumed
            if not self.arbitraryLookAhead() and inputConsumed(newstate, state):
                return newstate
            newstate2 = other(state)
            return newstate2 if isParseSuccess(newstate2) else mergeErrors(newstate, newstate2)
        return processor


    def arbitraryLookAhead(self):
        return self._arbitrary_look_ahead


    def __and__(self, other):
        '''First run 'self' parser, followed by 'other'. Returns a list
        of values returned by 'self' and 'other'.
        '''

        @Parser
        def processor(state):
            state = self(state)
            if isParseError(state):
                return state
            newstate = other(state)
            if isParseError(newstate):
                return newstate
            return setParseSuccessTree(newstate, filter(lambda x: x is not None,
                                                        [parseSuccessTree(state), parseSuccessTree(newstate)]))  # filter out 'skipped' input
        return processor


    def __ge__(self, f):
        '''Analogue to Haskell's '>>=' ('bind') member of Monad type class.
        Applies a parser 'self'. Then applies function 'f' to produce out of
        value returned by 'self' a new parser.
        '''

        @Parser
        def processor(state):
            newstate = self(state)
            if isParseError(newstate):
                return newstate
            tree = parseSuccessTree(newstate)
            return f(tree)(newstate)
        return processor


    def flatMap(self, f):
        '''Same as >= ('bind' operator)'''

        return self >= f


    def map(self, f):
        '''Same as fmap'''

        return self.flatMap(lambda x: lift(f(x)))


    def __rshift__(self, other):
        '''Analogue to Haskell's '>>' ('then') member of Monad type class.
        Applies parser 'self', ignoring the value returned by it. Then
        applies parser 'other'.
        '''

        return self.flatMap(lambda _: other)


    @staticmethod
    def lift(tree):
        '''Analogue to Haskell's 'return'. Takes a value 'tree'
        and creates a parser, which will result in a 'tree' for
        any state passed to the parser.
        Used when building parsers with monadic operations.
        However, it is ALWAYS possible to achieve the same
        functionality using 'syntax_tree(your_function)'
        decorator on a parser, which results in a applying
        'your_function' to the value returned by the parser.
        '''

        @Parser
        def processor(state):
            return setParseSuccessTree(state, tree)
        return processor


    @staticmethod
    def fmap(f, m):
        '''Analogue to Haskell's fmap member of Functor type class. Takes a
        function 'f' and a parser 'm'. Returns a new parser, which will
        apply 'f' to the value returned by the original parser.
        '''

        return m >= (lambda tree: lift(f(tree)))


    @staticmethod
    def tryP(parser):
        '''Takes a parser and returns a new parser with arbitrary look ahead.
        This ONLY changes the behavior of a new parser when using it with
        'choice' or '|' in the following way: if a new parser fails WITH
        consuming any input, the next alternative parser is nonetheless TRIED.
        '''

        return Parser(parser._parser, arbitrary_look_ahead=True)





lift  = Parser.lift
fmap  = Parser.fmap
tryP  = Parser.tryP
mzero = lift([])  # 'unit' parser: returns an empty list for any state




def syntax_tree(transform):
    # '''Decorator for the user to apply a 'transform' function to the tree
    # returned by the parser.'''
    '''Decorator to be applied to the parser. Returns a new parser,
    which will apply 'transform' function to the value returned by
    the original parser.
    NOTE: this is a way to build Abstract Syntax Trees from the values
    returned by the parsers.
    '''

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
    '''Runs a 'parser' over the 'input'. A 'parser' is either one of the
    many parsers provided by the library, or built by user with the help of
    library's combinators; 'input' is a string to parse; 'sourceName' is
    only used when displaying error messages (defaulted to None)
    '''

    state = parser(initialParseState(sourceName, input))

    return parseSuccessTree(state) if isParseSuccess(state) else showParseError(state)
