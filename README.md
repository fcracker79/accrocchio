[![build status](https://img.shields.io/travis/fcracker79/accrocchio/master.svg?style=flat-square)](https://travis-ci.org/fcracker79/accrocchio)

# accrocchio
Accrocchio is a library to mark and being notified of smelly code (a.k.a, "accrocchio").

Example
-------

```python
from accrocchio.badgeofshame import accrocchio
from accrocchio import observers


class AClassThatSmells(metaclass=accrocchio):
    pass

@accrocchio
def a_function_that_smells():
    pass


accrocchio.how_many()     # here we have 1, as you have declared a smelly class
AClassThatSmells()
accrocchio.how_many()     # here we have 2, as you have created an instance of a smelly class
a_function_that_smells()
accrocchio.how_many()     # here we have 3, as you have invoked a smelly function

accrocchio.reset()
accrocchio.how_many()     # here we have 0

# You can also be notified of smelly code execution, such as:

class MyAccrocchioObserver(observers.AccrocchioObserver):
    def on_accrocchio(self):
        print('Another accrocchio!')

    def reset(self):
        print('Reset accrocchi')
accrocchio.add_observer(MyAccrocchioObserver())
a_function_that_smells()   # prints 'Another accrocchio!'
accrocchio.reset()         # prints 'Reset accrocchi'

```

The library also implements ![Michael Duell's resign patterns](http://nishitalab.org/user/paulo/files/resign-patterns.txt).

```python
from accrocchio.badgeofshame import accrocchio, detonator


@accrocchio
def accrocchio_fun():
    pass


@detonator
def detonator_fun():
    pass


accrocchio_fun()
accrocchio.how_many()     # here we have 1, as you have invoked an accrocchio function
detonator.how_many()      # here we have 0, as you have never invoked a detonator function
detonator_fun()
detonator.how_many()      # here we have 1, as you have invoked a detonator function
accrocchio.how_many()     # here we have 2, as you have invoked a detonator function, which is an accrocchio

```

For a full list of the implemented accrocchio resign patterns, please consult ![Michael Duell's resign patterns](http://nishitalab.org/user/paulo/files/resign-patterns.txt).

Some final notes:
1. This library is useful only if a small part of the software is an accrocchio
2. We intentionally left out Python versions before 3.5, as we think they are a complete accrocchio.
3. We intentionally did not pass the accrocchio to the 'on_accrocchio' observer function, as you should treat all the accrocchios the same way
