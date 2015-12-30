from state import initialParseState
from state import isParseSuccess, parseSuccessTree, setParseSuccessTree




def syntax_tree(transform):
    '''Decorator for the user to apply a 'transform' function to the tree
    returned by the parser.'''
    def func(parser):
        def processor(state):
            newstate = parser(state)
            if isParseSuccess(newstate):
                tree = parseSuccessTree(newstate)
                return setParseSuccessTree(newstate, transform(tree))
            else:
                return newstate
        return processor
    return func



def parse(sourceName, parser, input):
    return parser(initialParseState(sourceName, input))
