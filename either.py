from math import sqrt, log
from utils import compose



class Either(object):

    def __init__(self, x):
        self.value = x
    
    def isLeft(self):
        return False

    def isRight(self):
        return False

    def getValue(self):
        return self.value

    def __repr__(self):
        return self.__str__()


    def __rshift__(self, other):
        return self >= (lambda x: other)


class Left(Either):
    def __init__(self, x):
        super(Left, self).__init__(x)


    def isLeft(self):
        return True

    
    def __ge__(self, g):
        return self

    def __str__(self):
        return 'Left ' + repr(self.getValue())


class Right(Either):
    def __init__(self, x):
        super(Right, self).__init__(x)

    def isRight(self):
        return True

    def __ge__(self, g):
        return g(self.getValue())

    def __str__(self):
        return 'Right ' + repr(self.getValue())



def either(f, g, m):
    x = m.getValue()
    return f(x) if m.isLeft() else g(x)



def fmapEither(f, m):
    return either(compose(Left, lambda x: x), compose(Right, f), m)
