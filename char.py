from string import ascii_letters
from combinators import choice, sequence, many1


def char_range(c1, c2):
    for c in xrange(ord(c1), ord(c2) + 1):
        yield chr(c)



def char(ch):
    def processor(text):
        if text and ch == text[0]:
            return (ch, text[1:])
    return processor


def string(s):
    return sequence(*map(char, s))


def oneOf(chars):
    return choice(*map(char, chars))


def noneOf(chars):
    return lambda text: (text[0], text[1:]) if oneOf(chars)(text) is None else None



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
