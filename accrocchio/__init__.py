import os
import sys
import types


class ThisModuleType(types.ModuleType):
    def __init__(self, *a, **kw):
        super(ThisModuleType, self).__init__(*a, **kw)
        self._imported = False

    @classmethod
    def _print_fake_this(cls):
        this_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
        this_path = os.path.join(this_dir, 'this.py')
        with open(this_path, 'r') as f:
            eval(''.join(f.readlines()))

    @property
    def __spec__(self):
        if not self._imported:
            self._imported = True
            self._print_fake_this()

sys.modules['this'] = ThisModuleType('this', 'Fake')
