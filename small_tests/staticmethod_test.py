class Foo(object):
    @staticmethod
    def bar(one, two):
        print(one, two)

a = Foo()
a.bar(a, 1)