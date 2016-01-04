from collections import namedtuple
from pos import initialPos, updatePosString



sourcePos, treeAttr, remainder = 'sourcepos', 'tree', 'remainder'

ParseSuccess = namedtuple('ParseSuccess', [sourcePos, treeAttr, remainder])



def updateParseSuccessField(state, field_name, new_value):
    return state._replace(**{field_name: new_value})



def setParseSuccessPos(state, pos):
    return updateParseSuccessField(state, sourcePos, pos)


def setParseSuccessTree(state, t):
    return updateParseSuccessField(state, treeAttr, t)


def setParseSuccessRemainder(state, rem):
    return updateParseSuccessField(state, remainder, rem)


def parseSuccessPos(state):
    return getattr(state, sourcePos)


def parseSuccessTree(state):
    return getattr(state, treeAttr)


def parseSuccessRemainder(state):
    return getattr(state, remainder)


def initialParseState(sourceName, input):
    return ParseSuccess(initialPos(sourceName), [], input)



def updateParseSuccess(state, stringProcessed, tree, remainder):
    newPos = updatePosString(parseSuccessPos(state), stringProcessed)
    return ParseSuccess(newPos, tree, remainder)
