import sys
import copy
import builtins
import traceback
# from queue import Queue
import queue
import threading
import time

################# look at me ################################
#  http://www.rueckstiess.net/research/snippets/show/ca1d7d90
#############################################################


class ReadOnlyBuiltins(dict):
        """
        Type used for a read only version of the __builtins__ dictionary.
        """
        # def __hash__(self):
        #     return hash(repr(self))

        def clear(self):
            ValueError("Read only!")

        def __delitem__(self, key):
            ValueError("Read only!")

        def pop(self, key, default=None):
            ValueError("Read only!")

        def popitem(self):
            ValueError("Read only!")

        def setdefault(self, key, default=None):
            ValueError("Read only!")

        def __setitem__(self, key, value):
            ValueError("Read only!")

        def update(self, dict, **kw):
            ValueError("Read only!")


def create_read_only_builtins(builtins_dict):
    """Substitutes given dictionary with a non modifiable version.

    Args:
        builtins_dict (dict): Dictionary to be modified.

    Returns:
        (dict): Non modifiable dictionary.

    """


    safe_builtins = ReadOnlyBuiltins(builtins_dict)

    def __init__(*args, **kw):
        ValueError("Read only!")

    ReadOnlyBuiltins.__init__ = __init__
    return safe_builtins


class SafeImport(object):
    """Creates safe replacement for builtin `__init__` function. Can import
    only from modules whitelist. It is created as a class, because
    `multiprocessing.Process` uses pickle for safekeeping, and you cannot
    pickle nested functions. `_safe_import` function needs to be nested, to use
    `module_whitelist` variable, which needs to be modified from the outside.

    Returns:
        (func): "Safe" import function.

    """
    def __init__(self):
        self.module_whitelist = ['time']

    def __call__(self, *args, **kwargs):
        return self._safe_import

    def _safe_import(self, module_name, globals={}, locals={},
                    fromlist=[], level=-1):
        if module_name in self.module_whitelist:
            return __import__(module_name, globals, locals,
                              fromlist, level)
        else:
            raise ImportError('Module \'' + module_name + '\' is not on '
                                                          'the import '
                                                          'whitelist')


def _safe_open(file, mode='r', buffering=-1, encoding=None,
              errors=None, newline=None, closefd=True):
    """Creates safe replacement for builtin `open` function.

    Todo:
        - Check for open modes, whether every destructive one will be
          blocked.
    """

    for char in mode:
        if char in ['w', 'a', '+']:
            raise IOError('Mode \'' + char + '\' is disallowed in the '
                                             'sandbox.')
    return open(file, mode, buffering, encoding,
                errors, newline, closefd)


def create_whitelist():
        """Creates builtins whitelist for `exec` environment.

        Returns:
            (set): Set of names to be whitelisted.

        """
        ret = set()

        def recurse(item):
            if item.__subclasses__():
                for sub_item in item.__subclasses__():
                    ret.add(sub_item.__name__)
                    recurse(sub_item)
                return
            ret.add(item.__name__)

        recurse(builtins.BaseException)

        constants = {'False',
                     'None',
                     'True',
                     '__doc__',
                     '__name__',
                     '__package__',
                     }

        types = {'basestring',
                 'bytearray',
                 'bytes',
                 'complex',
                 'dict',
                 'float',
                 'frozenset',
                 'int',
                 'long',
                 'object',
                 'set',
                 'str',
                 'tuple',
                 'unicode',
                 }

        functions = {'__import__',
                     'abs',
                     'all',
                     'any',
                     'ascii',
                     'apply',
                     'bin',
                     'bool',
                     'bytearray',
                     'bytes',
                     'callable',
                     'chr',
                     'classmethod',
                     'complex',
                     'dict',
                     'dir',
                     'divmod',
                     'enumerate',
                     'filter',
                     'float',
                     'format',
                     'frozenset',
                     'getattr',
                     'globals',
                     'hasattr',
                     'hash',
                     'help,'
                     'hex',
                     'id',
                     'input',
                     'int',
                     'isinstance',
                     'issubclass',
                     'iter',
                     'len',
                     'list',
                     'locals',
                     'map',
                     'max',
                     'min',
                     'next',
                     'object',
                     'oct',
                     'ord',
                     'pow',
                     'print',
                     'property',
                     'range',
                     'repr',
                     'reversed',
                     'round',
                     'set',
                     'setattr',
                     'slice',
                     'sorted',
                     'staticmethod',
                     'str',
                     'sum',
                     'super',
                     'tuple',
                     'type',
                     'vars',
                     'zip',
                     }

        ret = ret | constants | types | functions
        return ret


def _run(filename, new_builtins, queue):
    try:
        exec(open(filename).read(), {'__builtins__': dict(**new_builtins)}, {})
    except Exception as e:
        queue.put(e)
    return 0


class Runner(object):
    """Acts as a sandbox environment for user scripts. Aims to be as safe as
    possible. Uses `exec` for script execution.

    Possible circumventions:
        - Find `file` in a list of `object` class subclasses.
        - Impose one function on another by overwriting `func_code`

    """

    rtr = ''

    def __init__(self, builtins_expansion=None):
        self.current_run = None

        self.main = sys.modules['__main__'].__dict__
        self.orig_builtins = self.main['__builtins__'].__dict__

        # Build new builtins dictionary, from names whitelist
        self.builtins_whitelist = create_whitelist()
        self.new_builtins = dict()

        for item in self.orig_builtins.keys():
            if item in self.builtins_whitelist:
                self.new_builtins[item] = \
                    copy.deepcopy(self.orig_builtins[item])

        if builtins_expansion:
            self.new_builtins.update(builtins_expansion)

        # Remove items specified in blacklist from builtins
        self.builtins_blacklist = []

        for item in self.builtins_blacklist:
            if item in self.new_builtins.keys():
                self.new_builtins.pop(item)

        # Whitelist of module names, that can be imported into Runner scripts
        self.module_whitelist = []

        # Adding custom "safe" methods to new builtins
        self.safe_import_object = SafeImport()
        self.new_builtins['__import__'] = self.safe_import_object()
        self.new_builtins['open'] = _safe_open

        self.new_builtins = create_read_only_builtins(self.new_builtins)

    def run(self, filename, feedback=False, timeout=None):
        """Safely executes Python script located in user `home` directory.

        Todo:
            - Add return string (one way communication)
            - Cleanup implementation

        Args:
            filename (str): Name of the file containing the script.
            feedback (flag, bool): For printing query results into console
            timeout (int): Timeout in seconds after which the execution stops

        """
        run_queue = queue.Queue()
        # manager = multiprocessing.Manager()
        # new_builtins = manager.dict()
        # for key in self.new_builtins:
        #     new_builtins[key] = self.new_builtins[key]

        self.current_run = threading.Thread(target=_run, args=(filename,
                                                               self.new_builtins,
                                                               run_queue))

        try:
            self.current_run.daemon = True
            self.current_run.start()
            start_time = time.time()

            while self.current_run.is_alive():
                if time.time() - start_time > 3:
                    print('Killing process!')
                    self.current_run._stop()
                    print('> Killed!')
                    self.current_run._delete()
                    break
            else:
                print('> else')
                rtr_value = queue.get()
                if isinstance(rtr_value, BaseException):
                    raise rtr_value
                elif rtr_value is 0:
                    return 'return_string'
                else:
                    raise RuntimeError('something happened')
        except RuntimeError:
            raise
        except SyntaxError as e:
            e.filename = filename
            raise e
        except Exception as e:
            _, _, tb = sys.exc_info()
            line_number = str(traceback.extract_tb(tb)[-1][1])
            args = list(e.args)
            if len(args) > 0:
                args[0] = str(args[0]) + '\nIn file \"{}\", line {}' \
                    .format(filename, line_number)
                e.args = tuple(args)
            raise e

        # print('> Executed')
        # raise queue.get()

    def strop_current_run(self):
            # self.current_run
            pass

if __name__ == '__main__':
    ################################
    # THIS IS FOR TESTING PURPOSES #
    ################################
    box = Runner()
    box.run('E:\\test.py')
    # box.run_old('E:\\test.py')
