from deepdiff import DeepDiff


class Foo(object):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if DeepDiff(self, other):
            return False
        else:
            return True


class Bar(object):
    def __init__(self, name):
        self.name = name


a = Foo('adam')
b = Foo('adam')
c = Bar('adam')
d = Bar('adam')

print('a: ', a)
print('b: ', b)
print('c: ', c)
print('d: ', d)

print()
print('a == b: ', a == b)
print('a is b: ', a is b)
print()
print('a == a: ', a == a)
print('a is a: ', a is a)
print()
print('c == d: ', c == d)
print('c is d: ', c is d)
print()
print('c == c: ', c == c)
print('c is c: ', c is c)
print()

e = Bar('adam')


class Bar(object):
    def __init__(self, name):
        self.name = name
        self.something = 'sth'


f = Bar('adam')
print(DeepDiff(e, f))
