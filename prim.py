from state import initialParseState
from state import isParseSuccess, parseSuccessTree, setParseSuccessTree, showParseError
from combinators import Parser




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
