# *** COMBINATORS ***


from prim import Parser, syntax_tree, fmap, lift, mzero
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
            return tree if len(tree) != 2 else flatten(tree[0]) + [tree[1]]
        except TypeError:
            return tree
    return syntax_tree(flatten)(reduce(and_, parsers, mzero))



def choice(*parsers):
    try:
        return reduce(or_, parsers)
    except TypeError:
        return mzero



def between(open, close, parser):
    return open >> parser >= (lambda p: close >> lift(p))



def many1(parser):
    return parser >= (lambda head: fmap(lambda tail: [head] + tail, many(parser)))



def manyR(parser):
    '''same as 'many', but quickly overflows stack due to recursion limit'''
    return (parser >= (lambda head: fmap(lambda tail: [head] + tail, manyR(parser)))) | mzero



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
    return parser | lift(default_value)



concat  = lambda xs: sum(xs, [])
prepend = lambda head: lambda tail: [head] + tail



def sepBy1(parser, sep, keep=False):
    rest = fmap(concat, many(sequence(sep, parser))) if keep else many(sep >> parser)
    return parser >= (lambda h: fmap(prepend(h), rest))



def sepBy(parser, sep, keep=False):
    return option([], sepBy1(parser, sep, keep))



def endBy1(parser, sep, keep=False):
    if keep:
        parseOne, transform = sequence(parser, sep), concat
    else:
        parseOne, transform = parser >= (lambda p: sep >> lift(p)), lambda x: x
    return fmap(transform, many1(parseOne))



def endBy(parser, sep, keep=False):
    return option([], endBy1(parser, sep, keep))



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
    return sequence(*[parser for _ in xrange(n)]) if n > 0 else mzero
