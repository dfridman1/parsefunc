from success import (
    setParseSuccessPos,
    setParseSuccessTree,
    setParseSuccessRemainder,
    parseSuccessPos,
    parseSuccessTree,
    parseSuccessRemainder,
    initialParseState,
    updateParseSuccess
)


from error import (
    ParseError,
    showParseError,
    setParseErrorPos,
    setParseErrorMsg,
    parseErrorPos,
    parseErrorMsg,
    mergeErrors,
    mergeErrorsMany
)


from pos import sourceLine, sourceColumn



def stateLineColumn(state):
    pos =  parseSuccessPos(state) if isParseSuccess(state) else parseErrorPos(state)
    return sourceLine(pos), sourceColumn(pos)



def inputConsumed(state1, state2):
    '''Returns True if transition from state2 to state1 involved input consumption'''
    return stateLineColumn(state1) > stateLineColumn(state2)
    


def isParseSuccess(state):
    return hasattr(state, 'tree')


def isParseError(state):
    return not isParseSuccess(state)


def mplusStates(state1, state2):
    '''If at least one of the states is ParseSuccess, return the first one.
    Otherwise, merge errors'''
    if isParseSuccess(state1):
        return state1
    elif isParseSuccess(state2):
        return state2
    else:
        return mergeErrors(state1, state2)



def mplusStatesMany(*states):
    return reduce(mplusStates, states)



def parseErrorFromSuccessState(state, message, expected='', noneof=''):
    '''Creates a ParseError from a previos state (of type ParseSuccess)'''
    return ParseError(parseSuccessPos(state), message, expected, noneof)
