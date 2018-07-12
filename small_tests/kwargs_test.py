kwargs_dict = {'jeden': 'foka', 'dwa': 'ryba'}


def foo(jeden=None, dwa=None):
    print(jeden, dwa)


def bar(jeden=None):
    print(jeden)


def test_fun(**kwargs):
    print(kwargs['jeden'])


foo(**kwargs_dict)
# bar(**kwargs_dict)
test_fun(**kwargs_dict)