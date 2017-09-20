|build status|

accrocchio
==========

Accrocchio is a library to mark and being notified of smelly code
(a.k.a, "accrocchio").

Example
-------

.. code:: python

    from accrocchio.badgeofshame import accrocchio


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

    from accrocchio import observers


    class MyAccrocchioObserver(observers.AccrocchioObserver):
        def on_accrocchio(self):
            print('Another accrocchio!')

        def reset(self):
            print('Reset accrocchi')
    observers.add_accrocchio_observer(MyAccrocchioObserver())
    a_function_that_smells()   # prints 'Another accrocchio!'
    accrocchio.reset()         # prints 'Reset accrocchi'

We intentionally: 1. Left out Python versions before 3.5, as we think
they are a complete accrocchio. This library is useful only if a small
part of the software is an accrocchio 2. Did not pass the accrocchio to
the 'on\_accrocchio' observer function, as you should treat all the
accrocchios the same way

.. |build status| image:: https://img.shields.io/travis/fcracker79/accrocchio/master.svg?style=flat-square
   :target: https://travis-ci.org/fcracker79/accrocchio
