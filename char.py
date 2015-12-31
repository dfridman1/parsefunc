from string import ascii_letters
from combinators import choice, sequence, many1
from prim import syntax_tree

from state import (
    parseSuccessRemainder,
    updateParseSuccess,
    parseErrorFromSuccessState,
    isParseSuccess
)




def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2) + 1):
        yield chr(c)



        
def char(ch):
    def processor(state):
        text = parseSuccessRemainder(state)
        if text and text[0] == ch:
            return updateParseSuccess(state, ch, ch, text[1:])
        else:
            message  = 'EOF reached' if not text else text[0] + ' found'
            expected = ch
            return parseErrorFromSuccessState(state, message, expected=expected)
    return processor



def mkString(chars):
    return ''.join(chars)



def string(s):
    return syntax_tree(mkString)(sequence(*map(char, s)))



def oneOf(chars):
    return choice(*map(char, chars))



def noneOf(chars):
    def processor(state):
        rem = parseSuccessRemainder(state)
        if not rem:
            return parseErrorFromSuccessState(state, 'EOF reached', noneof=chars)
        for ch in chars:
            newstate = char(ch)(state)
            if isParseSuccess(newstate):
                message, noneof = '%s found' % ch, chars
                return parseErrorFromSuccessState(state, message, noneof=noneof)
        return updateParseSuccess(state, rem[0], rem[0], rem[1:])
    return processor
            
                



letter  = oneOf(ascii_letters)
letters = syntax_tree(mkString)(many1(letter))
digit   = oneOf(char_range('0', '9'))
digits  = syntax_tree(mkString)(many1(digit))
space   = char(' ')
spaces  = syntax_tree(mkString)(many1(space))
lparen  = char('(')
rparen  = char(')')
lbrace  = char('{')
rbrace  = char('}')
newline = char('\n')
tab     = char('\t')
