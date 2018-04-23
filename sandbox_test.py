import sys
sys.path.insert(0, 'E:\\LabManager\\src\\third_party')
from sandbox import Sandbox, SandboxConfig


def func(a, b):
    return 'hello'


class Foo(object):
    def __init__(self, age):
        self.age = age


sandbox = Sandbox(SandboxConfig('stdout'))

f = open('exec_file_test.py').read()

foo = Foo(31)

cod = compile(f, 'exec_file_test.py', 'exec')
exec(cod, {}, {})
# sandbox.execute(cod, locals={'foo': foo})
