from inspect import cleandoc


def new_print(val):
    print('Hello', val)

code_inner = cleandoc("""
    def bar():
        print(' Inner')
""")

with open('outer_test.py', 'w') as f:
    f.write(code_inner)

code_outer = cleandoc("""
    # import inner
    # print('Outer')
    # inner.bar()
    
    def foo():
        print('xD')
        
    if __name__ == '__main__':
        print('Main')
""")

_glob = {}
_loc = {}

exec(code_outer, _glob, _loc)


class NewModule: pass




locals().update({'hi': mod})
hi.foo()
