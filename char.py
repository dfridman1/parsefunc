from string import ascii_letters
from combinators import choice, sequence, many1
from state import *




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




def string(s):
    return sequence(*map(char, s))



def oneOf(chars):
    return choice(*map(char, chars))



def noneOf(chars):
    def processor(state):
        rem = parseSuccessRemainder(state)
        if not rem:
            return parseErrorFromSuccessState(state, 'EOF reached')
        for ch in chars:
            newstate = char(ch)(state)
            if isParseSuccess(newstate):
                message, noneof = '%s found' % ch, chars
                return parseErrorFromSuccessState(state, message, noneof=noneof)
        return updateParseSuccess(state, rem[0], rem[0], rem[1:])
    return processor
            
                



letter  = oneOf(ascii_letters)
letters = many1(letter)
digit   = oneOf(char_range('0', '9'))
digits  = many1(digit)
space   = char(' ')
spaces  = many1(space)
lparen  = char('(')
rparen  = char(')')
lbrace  = char('{')
rbrace  = char('}')
newline = char('\n')
