from string import ascii_lowercase, ascii_uppercase, whitespace
from combinators import choice, sequence, many1
from prim import Parser, syntax_tree

from state import (
    parseSuccessRemainder,
    updateParseSuccess,
    parseErrorFromSuccessState,
    isParseSuccess
)



EOF_MESSAGE        = 'unexpected end of input'
FOUND_MESSAGE      = 'found %r'
UNEXPECTED_MESSAGE = 'unexpected %r'



def satisfy(predicate,
            errorMsg='character %r does not satisfy the predicate',
            expected='',
            noneof=''):
    '''Succeeds for any character, which satisfies the predicate.
    Returns the parsed character.
    '''

    @Parser
    def processor(state):
        remainder = parseSuccessRemainder(state)
        if not remainder:
            return parseErrorFromSuccessState(state,
                                              EOF_MESSAGE,
                                              expected,
                                              noneof)
        ch = remainder[0]
        if not predicate(ch):
            try:
                message = errorMsg % ch
            except TypeError:
                message = errorMsg
            return parseErrorFromSuccessState(state,
                                              message,
                                              expected,
                                              noneof)
        else:
            return updateParseSuccess(state, ch, ch, remainder[1:])
    return processor




def char(ch):
    '''Parses a character 'ch'. Returns this character.'''

    return satisfy(lambda x: x == ch,
                   UNEXPECTED_MESSAGE,
                   expected=ch)



def mkString(chars):
    return ''.join(chars)



def string(s):
    '''Parses a string 's'. Returns it. '''

    return syntax_tree(mkString)(sequence(*map(char, s)))



def oneOf(chars):
    '''Parses one of the characters in 'chars'. Returns the parsed character.
    '''

    return choice(*map(char, chars))



def noneOf(chars):
    '''Succeeds if the current character is NOT in 'chars'. Returns
    the parsed character.
    '''

    return satisfy(lambda ch: ch not in chars,
                   errorMsg=FOUND_MESSAGE,
                   noneof=chars)






toString = syntax_tree(mkString)
isUpper  = lambda ch: ch >= 'A' and ch <= 'Z'
isLower  = lambda ch: ch >= 'a' and ch <= 'z'
isDigit  = lambda ch: ch >= '0' and ch <= '9'
DIGITS   = ''.join(map(str, xrange(10)))


anyChar  = satisfy(lambda _: True)

upper    = satisfy(isUpper,
                   errorMsg=UNEXPECTED_MESSAGE,
                   expected=ascii_uppercase)

lower    = satisfy(isLower,
                   errorMsg=UNEXPECTED_MESSAGE,
                   expected=ascii_lowercase)

letter   = lower | upper
letters  = toString(many1(letter))

digit    = satisfy(isDigit,
                   errorMsg=UNEXPECTED_MESSAGE,
                   expected=DIGITS)


digits   = toString(many1(digit))
alphaNum = letter | digit
space    = oneOf(set(whitespace))
spaces   = toString(many1(space))
lparen   = char('(')
rparen   = char(')')
lbrace   = char('{')
rbrace   = char('}')
newline  = char('\n')
tab      = char('\t')
lbracket = char('[')
rbracket = char(']')
langle   = char('<')
rangle   = char('>')
