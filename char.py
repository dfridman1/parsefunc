from string import ascii_lowercase, ascii_uppercase, whitespace
from combinators import choice, sequence, many1
from prim import Parser, syntax_tree

from state import (
    parseSuccessRemainder,
    updateParseSuccess,
    parseErrorFromSuccessState,
    isParseSuccess
)



EOF_MESSAGE = 'unexpected end of input'



def char(ch):
    '''Parses a characted 'ch'. Returns this character.'''

    @Parser
    def processor(state):
        text = parseSuccessRemainder(state)
        if text and text[0] == ch:
            return updateParseSuccess(state, ch, ch, text[1:])
        else:
            message  = EOF_MESSAGE if not text else 'unexpected %r' % text[0]
            expected = ch
            return parseErrorFromSuccessState(state, message, expected=expected)
    return processor



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
    the parsed chacacter.
    '''

    @Parser
    def processor(state):
        rem = parseSuccessRemainder(state)
        if not rem:
            return parseErrorFromSuccessState(state, EOF_MESSAGE, noneof=chars)
        for ch in chars:
            newstate = char(ch)(state)
            if isParseSuccess(newstate):
                message, noneof = '%s found' % ch, chars
                return parseErrorFromSuccessState(state, message, noneof=noneof)
        return updateParseSuccess(state, rem[0], rem[0], rem[1:])
    return processor



def satisfy(predicate):
    '''Succeeds for any character, which satisfies the predicate.
    Returns the parsed character.
    '''

    @Parser
    def processor(state):
        remainder = parseSuccessRemainder(state)
        if not remainder:
            return parseErrorFromSuccessState(state, EOF_MESSAGE)
        ch = remainder[0]
        if not predicate(ch):
            return parseErrorFromSuccessState(state, 'character %r does not satisfy the predicate' % ch)
        else:
            return updateParseSuccess(state, ch, ch, remainder[1:])
    return processor






toString = syntax_tree(mkString)


anyChar  = satisfy(lambda _: True)
upper    = oneOf(ascii_uppercase)
lower    = oneOf(ascii_lowercase)
letter   = lower | upper
letters  = toString(many1(letter))
digit    = oneOf(''.join(map(str, xrange(10))))
digits   = toString(many1(digit))
alphaNum = letter | digit
space    = oneOf(whitespace)
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
