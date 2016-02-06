from collections import namedtuple
from pos import sourceLine, sourceColumn, sourceName
from string import ascii_letters




sourcePos, errorMsg, oneOfChars, noneofChars = 'sorcePos', 'error', 'oneof', 'noneof'



ParseError = namedtuple('ParseError', [sourcePos, errorMsg, oneOfChars, noneofChars])




def updateParseErrorField(pError, field_name, new_value):
    return pError._replace(**{field_name: new_value})



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








LETTERS = set(ascii_letters)
DIGITS  = set(map(str, xrange(10)))




def showParseError(pError):
    msg = '\n'.join([showPositionInfo(pError), parseErrorMsg(pError)])
    oneof, noneof = set(parseErrorOneOf(pError)), set(parseErrorNoneOf(pError))

    if oneof or noneof:
        msg += '\nexpecting '
    if oneof and noneof:
        msg += '%s\n           OR %s' % (showOneOf(oneof), showNoneOf(noneof))
    elif oneof:
        msg += '%s' % showOneOf(oneof)
    elif noneof:
        msg += '%s' % showNoneOf(noneof)

    return msg



def showPositionInfo(pError):
    pos = parseErrorPos(pError)
    filename, line, col = sourceName(pos), sourceLine(pos), sourceColumn(pos)

    info = '"%s" ' % filename if filename is not None else ''
    info += '(line %d, column %d):' % (line, col)
    
    return info




def showErrorMessages(chars, prefix=None):
    msg = prefix + ' ' if prefix is not None else ''
    errors = showChars(chars)
    if not errors:
        return ''
    
    msg += ', '.join(errors[:-1])
    if len(msg) > 1:
        msg += ' or '
    msg += errors[-1]
    return msg




def showOneOf(chars):
    return showErrorMessages(chars)



def showNoneOf(chars):
    return showErrorMessages(chars, 'none of')



def showChars(chars):
    '''Given a set of chars, return a list of strings desribing 'chars' in error messages'''
    res = []
    if LETTERS.issubset(chars):
        res.append('letter')
        chars -= LETTERS
    if DIGITS.issubset(chars):
        res.append('digit')
        chars -= DIGITS
    if ' ' in chars:
        res.append('space')
        chars.remove(' ')
    if chars:
        res.extend(map(repr, chars))
    return res
