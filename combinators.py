# *** COMBINATORS ***


from state import (
    isParseError,
    isParseSuccess,
    parseSuccessTree,
    setParseSuccessTree,
    mergeErrorsMany,
    stateOccurresLater
)




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
    return option([], many1(parser))



def option(default_value, parser):
    def processor(state):
        newstate = parser(state)
        if isParseSuccess(newstate):
            return newstate
        elif stateOccurresLater(newstate, state):
            return newstate
        else:
            return setParseSuccessTree(state, default_value)
    return processor




def alternating(parser, sep, to_keep=0):
    '''If to_keep = 0 (1), keep what is produced by parser (sep)'''
    def processor(state):
        newstate = many1(sequence(parser, sep))(state)

        if isParseError(newstate):
            newstate = parser(state) if to_keep == 0 else choice(sep, parser)(state)
            if isParseError(newstate):
                return setParseSuccessTree(state, []) if to_keep == 0 else newstate
            else:
                tree = [parseSuccessTree(newstate)] if to_keep == 0 else []
                return setParseSuccessTree(newstate, tree)

        else:
            tree = map(lambda x: x[to_keep], parseSuccessTree(newstate))
            newstate = choice(sep, parser)(newstate)
            if isParseError(newstate):
                return newstate
            else:
                if to_keep == 0:
                    tree.append(parseSuccessTree(newstate))
                return setParseSuccessTree(newstate, tree)
    return processor




def sepBy(parser, sep):
    return alternating(parser, sep)



def endBy(parser, sep):
    def processor(state):
        newstate = parser(state)
        if isParseError(newstate):
            return setParseSuccessTree(state, [])
        else:
            tree = [parseSuccessTree(newstate)]
            newstate = alternating(sep, parser, to_keep=1)(newstate)
            if isParseError(newstate):
                return newstate
            else:
                tree.extend(parseSuccessTree(newstate))
                return setParseSuccessTree(newstate, tree)
    return processor
