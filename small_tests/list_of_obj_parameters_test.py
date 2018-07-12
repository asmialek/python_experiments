class Foo(object):
    def __init__(self, name):
        self.name = name


a = Foo('adam')
b = Foo('bartek')
c = Foo('cecyl')

print([x.name for x in [a, b, c]])
