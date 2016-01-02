class JSON(object):
    def __init__(self, value):
        self._value = value

    def getValue(self):
        return self._value


class Number(JSON):
    def __init__(self, num):
        super(Number, self).__init__(num)

    def __str__(self):
        return 'Number(%f)' % self.getValue()


class String(JSON):
    def __init__(self, string):
        super(String, self).__init__(string)

    def __str__(self):
        return 'String(%r)' % self.getValue()


class Bool(JSON):
    def __init__(self, b):
        super(Bool, self).__init__(b)

    def __str__(self):
        return 'Bool(%s)' % ('true' if self.getValue() else 'false')


class Null(JSON):
    def __init__(self):
        pass

    def __str__(self):
        return 'Null'


class Array(JSON):
    def __init__(self, values):
        super(Array, self).__init__(values)

    def __str__(self):
        return 'Array(%s)' % ', '.join(map(str, self.getValue()))


class Object(JSON):
    def __init__(self, pairs):
        # 'pairs' are assumed to be a list of key-value pairs
        super(Object, self).__init__(pairs)

    def __str__(self):
        return 'Object(%s)' % ', '.join(map(self._showPair, self.getValue()))

    def _showPair(self, p):
        key, value = p
        return '(%s, %s)' % (key, str(value))
