class Foo(object):
    def __init__(self):
        self.bar = 10

a = Foo()
a.__dict__['bar'] = 11
print(a.bar)
