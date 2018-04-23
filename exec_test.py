import sys
import copy


class Sandbox(object):
    def __init__(self, whitelist=True):
        self.main = sys.modules['__main__'].__dict__
        self.orig_builtins = self.main['__builtins__'].__dict__
        # TODO Expand white/blacklists
        self.builtins_whitelist = {'False', 'None', 'True', '__import__',
                                   'print', 'globals', 'locals', 'range'}
        self.builtins_blacklist = {'__import__', 'os'}
        self.module_whitelist = ['time']
        self.new_builtins = {}

        if whitelist:
            self.use_whitelist(self.orig_builtins)
        else:
            self.use_blacklist(self.orig_builtins)

        self.new_builtins['__import__'] = \
            self._safe_import(__import__, self.module_whitelist)

    @staticmethod
    def _safe_import(__import__, module_whitelist):
        def safe_import(module_name, globals={}, locals={},
                        fromlist=[], level=-1):
            print('Using custom import!')
            if module_name in module_whitelist:
                print('Module in whitelist!')
                return __import__(module_name, globals, locals,
                                  fromlist, level)
            else:
                raise ImportError('Module \'{}\' is not on whitelist'
                                  .format(module_name))
        return safe_import

    def use_whitelist(self, builtins_dict):
        for builtin in builtins_dict.keys():
            if builtin in self.builtins_whitelist:
                self.new_builtins[builtin] = \
                    copy.deepcopy(builtins_dict[builtin])

    def use_blacklist(self, builtins_dict):
        for builtin in builtins_dict.keys():
            if builtin not in self.builtins_blacklist:
                self.new_builtins[builtin] = \
                    copy.deepcopy(builtins_dict[builtin])

    def run(self, filename, *args, **kwargs):
        print('Executing file!')
        exec(open(filename).read(), {'__builtins__': self.new_builtins}, {})
        print('File executed!')


if __name__ == '__main__':
    box = Sandbox()
    sepa = '\n\n------------------------------------\n\n'
    # print(box.main, box.orig_builtins, box.new_builtins, sep=sepa)
    # box.module_whitelist = ['string', 'time']
    box.run('exec_file_test.py')
