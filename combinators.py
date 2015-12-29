# *** COMBINATORS ***




def sequence(*parsers):
    def processor(text):
        result = []
        for pr in parsers:
            try:
                matched_text, text = pr(text)
                result.append(matched_text)
            except TypeError:
                return None
        return (result, text)
    return processor



def choice(*parsers):
    def processor(text):
        for pr in parsers:
            m = pr(text)
            if m is not None:
                return m
    return processor




def many1(parser):
    def processor(text):
        m = parser(text)
        if m is None:
            return None
        first_match, text = m
        matched = [first_match]
        
        while True:
            try:
                matched_text, text = parser(text)
                matched.append(matched_text)
            except TypeError:
                break
        return matched, text
    return processor



def many(parser):
    return option(many1(parser))



def option(parser):
    def processor(text):
        m = parser(text)
        return m if m is not None else ([], text)
    return processor



def sepBy(parser, sep):
    def processor(text):
        try:
            match, text      = parser(text)
            rest_match, text = many(sequence(sep, parser))(text)
            return [match] + map(lambda x: x[1], rest_match), text
        except TypeError:
            return [], text
    return processor



def endBy(parser, sep):
    def processor(text):
        match, text = many(sequence(parser, sep))(text)
        return map(lambda x: x[0], match), text
    return processor
    


# def parseAtom(text):
#     return choice(letters, digits)(text)

# def parseList(text):
#     return sequence(char('('), sepBy(parseExpr, spaces), char(')'))(text)

# parseExpr = choice(parseAtom, parseList)


# print parseExpr('(4 8 9 (define x 10))')
