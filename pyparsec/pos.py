from collections import namedtuple



sourcename, line, column = 'sourceName', 'sourceLine', 'sourceColumn'


SourcePos = namedtuple('SourcePos', [sourcename, line, column])



def updatePosField(t, field_name, new_value):
    return t._replace(**{field_name: new_value})



def newPos(sourceName, line, column):
    return SourcePos(sourceName, line, column)


def initialPos(sourceName):
    return newPos(sourceName, 1, 1)


def setSourceName(pos, name):
    return updatePosField(pos, sourcename, name)


def setSourceLine(pos, n):
    return updatePosField(pos, line, n)


def setSourceColumn(pos, n):
    return updatePosField(pos, column, n)


def sourceName(pos):
    return getattr(pos, sourcename)


def sourceLine(pos):
    return getattr(pos, line)


def sourceColumn(pos):
    return getattr(pos, column)



def incSourceLine(pos, n):
    return updatePosField(pos, line, sourceLine(pos) + n)


def incSourceColumn(pos, n):
    return updatePosField(pos, column, sourceColumn(pos) + n)



def updatePosChar(pos, ch):
    if ch == '\n':
        return setSourceColumn(incSourceLine(pos, 1), 1)
    elif ch == '\t':
        col = sourceColumn(pos)
        return setSourceColumn(pos, col + 8 - ((col - 1) % 8))
    else:
        return incSourceColumn(pos, 1)



def updatePosString(pos, s):
    return reduce(updatePosChar, s, pos)
