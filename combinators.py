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
    def processor(state):
        newstate = parser(state)
        if isParseSuccess(newstate):
            return newstate
        elif stateOccurresLater(newstate, state):
            return newstate
        else:
            return setParseSuccessTree(state, default_value)
    return processor





def sepBy1(parser, sep):
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
    def processor(state):
        newstate = many1(sequence(parser, sep))(state)
        if isParseError(newstate):
            return newstate
        tree = map(lambda x: x[0], parseSuccessTree(newstate))
        return setParseSuccessTree(newstate, tree)
    return processor



def endBy(parser, sep):
    return option([], endBy1(parser, sep))
