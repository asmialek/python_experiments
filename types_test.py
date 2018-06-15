a = str()
b = int(False)
c = list()
d = None

# print(a, b, c, d)
#
# print(type(a), type(b), type(c), type(d))
#
# if type(a) is str:
#     print('yey')
#
# if type(d) is str:
#     print('yey')
#
#

a = '\x97'
b = '97'
print(b.encode('utf-8'))
print(bytes.fromhex(b))
