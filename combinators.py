# *** COMBINATORS ***


from prim import Parser, syntax_tree, fmap, pure
from operator import and_, or_
from state import (
    isParseError,
    isParseSuccess,
    parseSuccessTree,
    setParseSuccessTree,
    mergeErrorsMany,
    inputConsumed
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



def between(open, close, parser):
    return open >> parser >= (lambda p: close >> pure(p))



def many1(parser):
    return parser >= (lambda head: fmap(lambda tail: [head] + tail, many(parser)))



def manyR(parser):
    '''same as 'many', but quickly overflows stack due to recursion limit'''
    return (parser >= (lambda head: fmap(lambda tail: [head] + tail, manyR(parser)))) | pure([])



def many(parser):
    @Parser
    def processor(state):
        tree = []
        while True:
            newstate = parser(state)
            if isParseError(newstate):
                break
            tree.append(parseSuccessTree(newstate))
            state = newstate
        return setParseSuccessTree(state, tree) if not inputConsumed(newstate, state) else newstate
    return processor



def option(default_value, parser):
    return parser | pure(default_value)



def sepBy1(parser, sep):
    return parser >= (lambda h: fmap(lambda t: [h] + t, many(sep >> parser)))



def sepBy(parser, sep):
    return option([], sepBy1(parser, sep))



def endBy1(parser, sep):
    parseOne = parser >= (lambda p: sep >> pure(p))
    return many1(parseOne)



def endBy(parser, sep):
    return option([], endBy1(parser, sep))



def skipMany1(parser):
    return parser >> skipMany(parser)


def skipMany(parser):
    @Parser
    def processor(state):
        newstate = many(parser)(state)
        if isParseSuccess(newstate):
            newstate = setParseSuccessTree(newstate, None)
        return newstate
    return processor



def count(n, parser):
    return sequence(*[parser for _ in xrange(n)]) if n > 0 else pure([])
