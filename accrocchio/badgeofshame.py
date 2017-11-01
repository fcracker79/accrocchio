import typing
from functools import wraps

import sys

from accrocchio import observers


_ACCROCCHI_COUNTS_FIELD = '_accrocchi_count'


def _reset_accrocchio(accrocchio_name: str):
    if accrocchio_name == 'accrocchio':
        setattr(_notify_accrocchio, _ACCROCCHI_COUNTS_FIELD, {})
    else:
        _get_accrocchi_counts().pop(accrocchio_name, 0)


def _get_accrocchi_counts() -> typing.Dict[str, int]:
    if not hasattr(_notify_accrocchio, _ACCROCCHI_COUNTS_FIELD):
        setattr(_notify_accrocchio, _ACCROCCHI_COUNTS_FIELD, {})
    return getattr(_notify_accrocchio, _ACCROCCHI_COUNTS_FIELD)


def _notify_accrocchio(accrocchio_name: str):
    accrocchi_counts = _get_accrocchi_counts()
    if accrocchio_name in accrocchi_counts:
        accrocchi_counts[accrocchio_name] += 1
    else:
        accrocchi_counts[accrocchio_name] = 1
    for o in observers.ACCROCCHIO_OBSERVERS.get(accrocchio_name, []):
        o.on_accrocchio()

    if accrocchio_name != 'accrocchio':
        _notify_accrocchio('accrocchio')


def _count(accrocchio_name: str):
    return _get_accrocchi_counts().get(accrocchio_name, 0)


class MetaAccrocchioForContext(type):
    def __enter__(cls):
        _notify_accrocchio(cls.__name__)
        return cls

    def __exit__(cls, exc_type, exc_val, exc_tb):
        pass


# noinspection PyPep8Naming
class accrocchio(type, metaclass=MetaAccrocchioForContext):
    def __new__(mcs, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            fun = args[0]
            if type(fun) == type:

                fun = fun.__init__

            @wraps(fun)
            def _inner(*a, **kw):
                try:
                    return fun(*a, **kw)
                finally:
                    _notify_accrocchio(mcs.__name__)

            if type(args[0]) == type:
                args[0].__init__ = _inner
                # noinspection PyProtectedMember
                _notify_accrocchio(mcs.__name__)
                return args[0]
            return _inner
        else:
            # noinspection PyProtectedMember
            _notify_accrocchio(mcs.__name__)
            result = super(accrocchio, mcs).__new__(mcs, *args, **kwargs)
            result.__accrocchio_name__ = mcs.__name__
            return result

    def __call__(cls, *args, **kwargs):
        # noinspection PyProtectedMember
        _notify_accrocchio(cls.__accrocchio_name__)
        return super(accrocchio, cls).__call__(*args, **kwargs)

    @classmethod
    def how_many(mcs):
        return _count(mcs.__name__)

    @classmethod
    def add_observer(mcs, observer: observers.AccrocchioObserver):
        observers.add_accrocchio_observer(observer, mcs.__name__)

    @classmethod
    def reset(mcs):
        observers.reset(mcs.__name__)
        _reset_accrocchio(mcs.__name__)


_PATTERNS = {
    'abject_poverty':
'''
The Abject Poverty Pattern is evident in software that is so difficult
to test and maintain that doing so results in massive budget overruns.
''',
    'blinder':
'''
The Blinder Pattern is an expedient solution to a problem without
regard for future changes in requirements. It is unclear as to whether
the Blinder is named for the blinders worn by the software designer
during the coding phase, or the desire to gouge his eyes out during
the maintenance phase.
''',
    'fallacy_method':
'''
The Fallacy method is evident in handling corner cases. The logic
looks correct, but if anyone actually bothers to test it, or if a
corner case occurs, the Fallacy of the logic will become known.
''',
    'prototry':
'''
The ProtoTry Pattern is a quick and dirty attempt to develop a working
model of software. The original intent is to rewrite the ProtoTry,
using lessons learned, but schedules never permit. The ProtoTry is
also known as legacy code.
''',
    'simpleton':
'''
The Simpleton Pattern is an extremely complex pattern used for the
most trivial of tasks. The Simpleton is an accurate indicator of the
skill level of its creator.
''',
    'adopter':
'''
The Adopter Pattern provides a home for orphaned functions. The result
is a large family of functions that don't look anything alike, whose
only relation to one another is through the Adopter.
''',
    'brig':
'''
The Brig Pattern is a container class for bad software. Also known as
module.
''',
    'compromise':
'''
The Compromise Pattern is used to balance the forces of schedule vs.
quality. The result is software of inferior quality that is still
late.
''',
    'detonator':
'''
The Detonator is extremely common, but often undetected. A common
example is the calculations based on a 2 digit year field. This bomb
is out there, and waiting to explode!
''',
    'fromage':
'''
The Fromage Pattern is often full of holes. Fromage consists of cheesy
little software tricks that make portability impossible. The older
this pattern gets, the riper it smells.
''',
    'flypaper':
'''
The Flypaper Pattern is written by one designer and maintained by
another. The designer maintaining the Flypaper Pattern finds herself
stuck, and will likely perish before getting loose.
''',
    'epoxy':
'''
The ePoxy Pattern is evident in tightly coupled software modules. As
coupling between modules increases, there appears to be an epoxy bond
between them.
''',
    'chain_of_possibilities':
'''
The Chain of Possibilities Pattern is evident in big, poorly
documented modules. Nobody is sure of the full extent of its
functionality, but the possibilities seem endless. Also known as
Non-Deterministic.
''',
    'commando':
'''
The Commando Pattern is used to get in and out quick, and get the job
done. This pattern can break any encapsulation to accomplish its
mission. It takes no prisoners.
''',
    'intersperser':
'''
The Intersperser Pattern scatters pieces of functionality throughout a
system, making a function impossible to test, modify, or understand.
''',
    'instigator':
'''
The Instigator Pattern is seemingly benign, but wreaks havoc on other
parts of the software system.
''',
    'momentum':
'''
The Momentum Pattern grows exponentially, increasing size, memory
requirements, complexity, and processing time.
''',
    'medicator':
'''
The Medicator Pattern is a real time hog that makes the rest of the
system appear to be medicated with strong sedatives.
''',
    'absolver':
'''
The Absolver Pattern is evident in problem ridden code developed by
former employees. So many historical problems have been traced to this
software that current employees can absolve their software of blame by
claiming that the absolver is responsible for any problem
reported. Also known as It's-not-in-my-code.
''',
    'stake':
'''
The Stake Pattern is evident in problem ridden software written by
designers who have since chosen the management ladder. Although
fraught with problems, the manager's stake in this software is too
high to allow anyone to rewrite it, as it represents the pinnacle of
the manager's technical achievement.
''',
    'eulogy':
'''
The Eulogy Pattern is eventually used on all projects employing the
other 22 Resign Patterns. Also known as Post Mortem.
''',
    'tempest_method':
'''
The Tempest Method is used in the last few days before software
delivery. The Tempest Method is characterized by lack of comments, and
introduction of several Detonator Patterns.
''',
    'visitor_from_hell':
'''
The Visitor From Hell Pattern is coincident with the absence of run
time bounds checking on arrays. Inevitably, at least one control loop
per system will have a Visitor From Hell Pattern that will overwrite
critical data.
'''
}

for pattern_name, docstring in _PATTERNS.items():
    setattr(
        sys.modules[__name__], pattern_name,
        type(pattern_name, (accrocchio, ), {'__doc__': docstring}))


_AccrocchioType = typing.TypeVar('Accrocchio', bound=accrocchio)


def this_is_a(accrocchio_type: typing.Type[_AccrocchioType]):
    _notify_accrocchio(accrocchio_type.__name__)


def this_is_an(accrocchio_type: typing.Type[_AccrocchioType]):
    return this_is_a(accrocchio_type)
