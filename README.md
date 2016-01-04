### Parser combinator library for Python
---

A recursive descent parser based on functional combinators. API closely follows
that of Parsec (a parsing library for Haskell). The library provides the user with
a wide range of combinators for building more complex parsers.

#### Example
---
Suppose we would like to parse and evaluate arithmetic expressions adhering to
this simple context-free grammar:
```
    EXPR   => TERM + EXPR | TERM
    TERM   => FACTOR * TERM | FACTOR
    FACTOR => integer | ( EXPR )
```

Now, we can see that EXPR is just a sum of TERM's and TERM is a product
of FACTOR's. High level of abstraction allows us to describe the parsers
in terms of what they actually are rather than hardcoding them.

Let's first define parsers for `+` and `*`. They would be
```
    plus, mult = char('+'), char('*')
```
To parse an expression, we can write

```
    def parseExpr(s):
        return sepBy(parseTerm, plus)(s)
```

This returns a list of values returned by parser `parseTerm`. Since our goal
is to write an evaluator, we can add a `syntax_tree(f)` decorator, which
takes a value returned by the parser and applies `f` to it. Since we have a
list of summands, we can apply `sum` to it to get:

```
    @syntax_tree(sum)
    def parseExpr(s):
        return sepBy(parseTerm, plus)(s)
```

`parseTerm` is almost identical to `parseExpr`, but with multiplication
replacing summation. Here's code for it:

```
    @syntax_tree(product)
    def parseTerm(s):
        return sepBy(parseFactor, mult)(s)
```

where `product = lambda factors: reduce(lambda x, y: x * y, factors, 1)`.

Finally, to parse a `FACTOR`, we define

```
    @Parser
    def parseFactor(s):
        return (parens(parseExpr) | integer)(s)
```

Note `Parser` decorator instead of `syntax_tree`. When defining a combinator
with a `def` keyword, it is **necessary** to decorate it with one of above
decorators to make it an object of class `Parser`. `@Parser` is equivalent to
`@syntax_tree(lambda x: x)`.

Now that we have the description of our small language defined, it is time to
call a top-level function `parse`, which takes a parser, text to parse, and
optionally the 'source name'.

```
    input = '5+(4+3)*(2*4+3)  # == 82
    print parse(parseExpr, input, sourceName='arithm.py') # == 82
```

Note that the above implementation does not allow spaces between tokens. For
a more rigorous treatment of evaluating arithmetic expressions, please go
[here](examples/arithm.py).


### Navigation
---
Please consult [combinators.py](combinators.py), [char.py](char.py) and [tokens.py](tokens.py)
for a wide range of combinators available.

[examples](examples) directory contains 2 examples of using the library:
- an extension to the arithmetic evaluator example laid out above
- json parser


### Notes

A more comprehensive documentation is soon to be released.
