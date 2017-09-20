from functools import wraps

from accrocchio import observers


def _notify_accrocchio():
    if not hasattr(_notify_accrocchio, 'count'):
        _notify_accrocchio.count = 1
    else:
        _notify_accrocchio.count += 1
    for o in observers.ACCROCCHIO_OBSERVERS:
        o.on_accrocchio()


def _count():
    return getattr(_notify_accrocchio, 'count', 0)


# noinspection PyPep8Naming
class accrocchio(type):
    def __new__(mcs, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            fun = args[0]

            @wraps(fun)
            def _inner(*a, **kw):
                try:
                    return fun(*a, **kw)
                finally:
                    _notify_accrocchio()

            return _inner
        else:
            # noinspection PyProtectedMember
            _notify_accrocchio()
            return super(accrocchio, mcs).__new__(mcs, *args, **kwargs)

    def __call__(cls, *args, **kwargs):
        # noinspection PyProtectedMember
        _notify_accrocchio()
        return super(accrocchio, cls).__call__(*args, **kwargs)

    @classmethod
    def how_many(mcs):
        return _count()

    @classmethod
    def reset(mcs):
        observers.reset()
        _notify_accrocchio.count = 0
