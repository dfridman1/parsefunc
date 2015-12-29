def compose(*functions):
    "Returns a new function, which is a composition of 'functions'"
    return lambda x: reduce(lambda val, f: f(val), reversed(functions), x)
