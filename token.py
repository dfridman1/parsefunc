from char import lparen, rparen
from combinators import sequence



def enclose(open, parser, close):
    def processor(text):
        try:
            (_, body, _), text = sequence(open, parser, close)(text)
            return body, text
        except TypeError:
            return None
    return processor


def parens(parser):
    return enclose(lparen, parser, rparen)


def braces(parser):
    return enclose(lbrace, parser, rbrace)
