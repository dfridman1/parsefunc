from collections import namedtuple
from utils import updateField
from pos import sourceLine, sourceColumn


sourcePos, errorMsg = 'sorcePos', 'error'

ParseError = namedtuple('ParseError', [sourcePos, errorMsg])



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



def mergeErrors(p1, p2):
    '''Returns an error, which occurres further down the input.'''
    pos1, pos2 = parseErrorPos(p1), parseErrorPos(p2)
    
    x = sourceLine(pos1), sourceColumn(pos1)
    y = sourceLine(pos2), sourceColumn(pos2)

    return p1 if x > y else p2



def mergeErrorsMany(*errors):
    return reduce(mergeErrors, errors)
