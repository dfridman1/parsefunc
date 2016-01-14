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






def _sequence(*parsers):
    '''same as 'sequence', but less efficient (due to having to
    ALWAYS go over all 'parsers'.
    '''

    def flatten(tree):
        try:
            return tree if len(tree) != 2 else flatten(tree[0]) + [tree[1]]
        except TypeError:
            return tree
    return syntax_tree(flatten)(reduce(and_, parsers, mzero))



def sequence(*parsers):
    '''Applies 'parsers' in sequence. Returns a list of values returned
    by parsers.
    '''

    @Parser
    def processor(state):
        tree = []
        for pr in parsers:
            state = pr(state)
            if isParseError(state):
                return state
            tree.append(parseSuccessTree(state))
        return setParseSuccessTree(state, tree)
    return processor



def _choice(*parsers):
    '''same as 'choice', but less efficient (due to having to
    ALWAYS go over all 'parsers'.
    '''

    try:
        return reduce(or_, parsers)
    except TypeError:
        return mzero



def choice(*parsers):
    '''Applies the parsers from 'parsers' in order, until one of them
    succeeds. Returns the value of the succeeding parser. If none of the
    parsers succeed, the error that occurres 'the farthest' into
    the input, is returned.
    '''

    @Parser
    def processor(state):
        errors = []
        for pr in parsers:
            newstate = pr(state)
            if isParseSuccess(newstate):
                return newstate
            # fail if any input has been consumed
            if not pr.arbitraryLookAhead() and inputConsumed(newstate, state):
                return newstate
            errors.append(newstate)
        return mergeErrorsMany(*errors)
    return processor



def between(open, close, parser):
    '''Parses 'open' -> 'parser' -> 'close'. Returns the value returned
    by 'parser'.
    '''

    return open >> parser >= (lambda p: close >> lift(p))



def many1(parser):
    '''Runs 'parser' one or more times. Returns a list of results
    returned py 'parser'.
    '''

    return parser >= (lambda head: fmap(lambda tail: [head] + tail, many(parser)))



def manyR(parser):
    '''same as 'many', but quickly overflows stack due to recursion limit'''

    return (parser >= (lambda head: fmap(lambda tail: [head] + tail, manyR(parser)))) | mzero



def many(parser):
    '''Runs 'parser' zero or more times. Returns a list of values
    returned by 'parser'.
    '''

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
    '''Runs 'parser' and returns a value returned by it. If parsing failed,
    returns 'default_value'.
    '''

    return parser | lift(default_value)



concat  = lambda xs: sum(xs, [])
prepend = lambda head: lambda tail: [head] + tail



def sepBy1(parser, sep, keep=False):
    '''Parses one or more occurrences of 'parser', separated by 'sep'.
    If keep is True, returns a list of values returned by BOTH 'parser'
    and 'sep'; otherwise, a list of values returned by 'parser'.
    '''

    rest = fmap(concat, many(sequence(sep, parser))) if keep else many(sep >> parser)
    return parser >= (lambda h: fmap(prepend(h), rest))



def sepBy(parser, sep, keep=False):
    '''Parses zero or more occurrences of 'parser', separated by 'sep'.
    If keep is True, returns a list of values returned by BOTH 'parser'
    and 'sep'; otherwise, a list of values returned by 'parser'.
    '''

    return option([], sepBy1(parser, sep, keep))



def endBy1(parser, sep, keep=False):
    '''Parses one or more occurrences of 'parser', separated and ended
    by 'sep'. If keep is True, returns a list of values returned by
    BOTH 'parser' and 'sep'; otherwise, a list of values returned by
    'parser'.
    '''

    if keep:
        parseOne, transform = sequence(parser, sep), concat
    else:
        parseOne, transform = parser >= (lambda p: sep >> lift(p)), lambda x: x
    return fmap(transform, many1(parseOne))



def endBy(parser, sep, keep=False):
    '''Parses zero or more occurrences of 'parser', separated and ended
    by 'sep'. If keep is True, returns a list of values returned by
    BOTH 'parser' and 'sep'; otherwise, a list of values returned by
    'parser'.
    '''

    return option([], endBy1(parser, sep, keep))



def skipMany1(parser):
    '''Applies 'parser' one or more times, ignoring the result.'''

    return parser >> skipMany(parser)



def skipMany(parser):
    '''Applies 'parser' zero or more times, ignoring the result.'''

    @Parser
    def processor(state):
        newstate = many(parser)(state)
        if isParseSuccess(newstate):
            newstate = setParseSuccessTree(newstate, None)
        return newstate
    return processor



def count(n, parser):
    '''Applies 'parser' n times. Returns a list of n values returned by
    'parser'. If n <= 0, returns [].
    '''

    return sequence(*[parser for _ in xrange(n)]) if n > 0 else mzero
