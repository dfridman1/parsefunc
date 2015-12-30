from state import initialParseState






def parse(sourceName, parser, input):
    return parser(initialParseState(sourceName, input))
