from char import lparen, rparen, lbrace, rbrace
from combinators import sequence
from state import isParseError, parseSuccessTree, setParseSuccessTree




def enclose(open, parser, close):
    def processor(state):
        newstate = sequence(open, parser, close)(state)
        if isParseError(newstate):
            return newstate
        parser_tree = parseSuccessTree(newstate)[1]
        return setParseSuccessTree(newstate, parser_tree)
    return processor



def parens(parser):
    return enclose(lparen, parser, rparen)


def braces(parser):
    return enclose(lbrace, parser, rbrace)
