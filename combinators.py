# *** COMBINATORS ***


from prim import Parser, syntax_tree
from operator import and_, or_
from state import (
    isParseError,
    isParseSuccess,
    parseSuccessTree,
    setParseSuccessTree,
    mergeErrorsMany,
    stateOccurresLater
)








def sequence(*parsers):
    def flatten(tree):
        try:
            return tree if len(tree) <> 2 else flatten(tree[0]) + [tree[1]]
        except TypeError:
            return tree
    return syntax_tree(flatten)(reduce(and_, parsers))




def choice(*parsers):
    return reduce(or_, parsers)



def many1(parser):
    @Parser
    def processor(state):
        state = parser(state)
        if isParseError(state):
            return state
        tree = [parseSuccessTree(state)]
        while True:
            newstate = parser(state)
            if isParseError(newstate):
                break
            tree.append(parseSuccessTree(newstate))
            state = newstate
        return newstate if stateOccurresLater(newstate, state) else setParseSuccessTree(state, tree)
        
    return processor




def many(parser):
    return option([], many1(parser))



def option(default_value, parser):
    @Parser
    def processor(state):
        newstate = parser(state)
        if isParseSuccess(newstate) or stateOccurresLater(newstate, state):
            return newstate
        else:
            return setParseSuccessTree(state, default_value)
    return processor





def sepBy1(parser, sep):
    @Parser
    def processor(state):
        state = parser(state)
        if isParseError(state):
            return state
        tree = [parseSuccessTree(state)]
        state = many(sequence(sep, parser))(state)
        if isParseError(state):
            return state
        tree.extend(map(lambda x: x[1], parseSuccessTree(state)))
        return setParseSuccessTree(state, tree)
    return processor




def sepBy(parser, sep):
    return option([], sepBy1(parser, sep))



def endBy1(parser, sep):
    @Parser
    def processor(state):
        newstate = many1(sequence(parser, sep))(state)
        if isParseError(newstate):
            return newstate
        tree = map(lambda x: x[0], parseSuccessTree(newstate))
        return setParseSuccessTree(newstate, tree)
    return processor



def endBy(parser, sep):
    return option([], endBy1(parser, sep))
