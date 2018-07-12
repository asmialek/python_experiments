"""
Supercool test for singleton decorator. Use it instead of writing your
convoluted own singleton stuff. Srsly, it's cool.
"""

from singleton_decorator import singleton


@singleton
class foo(object):
    def __init__(self):
        self.var = None

a = foo()
a.var = 'adam'
print(a.var)
b = foo()
print(b.var)
b.var = 'dominika'
print(a.var)
