from char import (
    lparen,
    rparen,
    lbrace,
    rbrace,
    lbracket,
    rbracket,
    langle,
    rangle,
    space,
    char,
    digits,
    oneOf
)
from combinators import (
    between,
    many,
    skipMany,
    sepBy,
    sepBy1,
    option,
    sequence
)
from prim import (
    lift,
    fmap,
    tryP
)




def between_(open, close):
    open, close = sequence(open, many(space)), sequence(many(space), close)
    return lambda parser: between(open, close, parser)


parens   = between_(lparen, rparen)
braces   = between_(lbrace, rbrace)
angles   = between_(langle, rangle)
brackets = between_(lbracket, rbracket)


whiteSpace = skipMany(space)


def trailing_space(parser):
    "Skips trailing whitespace"
    return parser >= (lambda p: whiteSpace >> lift(p))


comma = trailing_space(char(','))
semi  = trailing_space(char(';'))
colon = trailing_space(char(':'))
dot   = trailing_space(char('.'))



sepBy_  = lambda sep: lambda parser: sepBy(parser, sep)
sepBy1_ = lambda sep: lambda parser: sepBy1(parser, sep)

semiSep  = sepBy_(semi)
semiSep1 = sepBy1_(semi)

commaSep  = sepBy_(comma)
commaSep1 = sepBy1_(comma)



def updateSign(sign, num):
    return num * (-1 if sign == '-' else 1)


natural         = fmap(int, digits)

integer         = fmap(lambda x: updateSign(*x),
                       sequence(option('', oneOf('-+')), natural))

doublePos       = fmap(lambda x: float(''.join(x)),
                       sequence(digits, char('.'), option('0', digits)))

double          = fmap(lambda x: updateSign(*x),
                       sequence(option('', oneOf('-+')), doublePos))

integerOrDouble = tryP(double) | integer
