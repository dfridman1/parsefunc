from collections import namedtuple
from utils import updateField
from pos import sourceLine, sourceColumn




sourcePos, errorMsg, oneOfChars, noneofChars = 'sorcePos', 'error', 'oneof', 'noneof'



ParseError = namedtuple('ParseError', [sourcePos, errorMsg, oneOfChars, noneofChars])



def updateParseErrorField(pError, field_name, new_value):
    return updateField(ParseError, pError, field_name, new_value)



def setParseErrorPos(pError, pos):
    return updateParseErrorField(pError, sourcePos, pos)



def setParseErrorMsg(pError, msg):
    return updateParseErrorField(pError, errorMsg, msg)



def parseErrorPos(pError):
    return getattr(pError, sourcePos)


def parseErrorMsg(pError):
    return getattr(pError, errorMsg)


def parseErrorOneOf(pError):
    return getattr(pError, oneOfChars)


def parseErrorNoneOf(pError):
    return getattr(pError, noneofChars)



def mergeErrors(p1, p2):
    '''Returns an error, which occurres further down the input.'''
    pos1, pos2 = parseErrorPos(p1), parseErrorPos(p2)
    
    x = sourceLine(pos1), sourceColumn(pos1)
    y = sourceLine(pos2), sourceColumn(pos2)

    if x > y:
        return p1
    elif y > x:
        return p2
    else:
        return concatErrors(p1, p2)



def concatErrors(p1, p2):
    mergedOneOf  = parseErrorOneOf(p1) + parseErrorOneOf(p2)
    mergedNoneOf = parseErrorNoneOf(p1) + parseErrorNoneOf(p2)

    return ParseError(parseErrorPos(p1),
                      parseErrorMsg(p1),
                      mergedOneOf,
                      mergedNoneOf)

    


def mergeErrorsMany(*errors):
    return reduce(mergeErrors, errors)
