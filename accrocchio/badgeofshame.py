from functools import wraps

from accrocchio import observers


class accrocchio:
    def __init__(self, fun):
        @wraps(fun)
        def _inner(*a, **kw):
            try:
                return fun(*a, **kw)
            finally:
                if not hasattr(accrocchio, 'count'):
                    accrocchio.count = 1
                else:
                    accrocchio.count += 1
                for o in observers.ACCROCCHIO_OBSERVERS:
                    o.on_accrocchio()
        self._inner = _inner

    def __call__(self, *args, **kwargs):
        return self._inner(*args, **kwargs)

    @classmethod
    def how_many(cls):
        return getattr(accrocchio, 'count', 0)

    @classmethod
    def reset(cls):
        observers.reset()
        accrocchio.count = 0
