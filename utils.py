def compose(*functions):
    "Returns a new function, which is a composition of 'functions'"
    return lambda x: reduce(lambda val, f: f(val), reversed(functions), x)




def updateField(name, t, field_name, new_value):
    '''Returns a new namedtuple named 'name' similar to 't', but with
    'new_value' replacing corresponding value at 'field_name\''''
    return name(*[new_value if field == field_name else getattr(t, field)
                  for field in t._fields])
