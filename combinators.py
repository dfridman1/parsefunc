# *** COMBINATORS ***


from state import *



def sequence(*parsers):
    def processor(state):
        tree = []
        for pr in parsers:
            state = pr(state)
            if isParseError(state):
                return state
            tree.append(parseSuccessTree(state))
        return setParseSuccessTree(state, tree)
    return processor




def choice(*parsers):
    def processor(state):
        errors = []
        for pr in parsers:
            newstate = pr(state)
            if isParseSuccess(newstate):
                return newstate
            errors.append(newstate)
        return mergeErrorsMany(*errors)
    return processor



def many1(parser):
    def processor(state):
        at_least_one, tree = False, []
        while True:
            newstate = parser(state)
            if isParseError(newstate):
                break
            tree.append(parseSuccessTree(newstate))
            state, at_least_one = newstate, True
        return setParseSuccessTree(state, tree) if at_least_one else newstate
    return processor




def many(parser):
    return option(many1(parser))


def option(parser):
    def processor(state):
        newstate = parser(state)
        return newstate if isParseSuccess(newstate) else state
    return processor




def sepBy(parser, sep):
    def processor(state):
        newstate = parser(state)
        if isParseError(newstate):
            return newstate
        tree     = [parseSuccessTree(newstate)]
        newstate = many(sequence(sep, parser))(newstate)
        tree.extend(map(lambda x: x[1], parseSuccessTree(newstate)))  # get rid of 'sep' component
        return setParseSuccessTree(newstate, tree)
    return processor



def endBy(parser, sep):
    def processor(state):
        newstate = many(sequence(parser, sep))(state)
        tree     = map(lambda x: x[0], parseSuccessTree(newstate))  # get rid of 'sep' component
        return setParseSuccessTree(newstate, tree)
    return processor
