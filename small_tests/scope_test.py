import sys
import time

print(sys.path)
def Foo():
    sys.path = []
    print(sys.path)
Foo()
print(sys.path)
