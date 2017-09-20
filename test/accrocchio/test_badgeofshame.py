import unittest
from unittest import mock

from accrocchio import observers
from accrocchio.badgeofshame import accrocchio, Accrocchio
from accrocchio.observers import AccrocchioObserver


class TestBadgeOfShame(unittest.TestCase):
    def setUp(self):
        accrocchio.reset()
        assert accrocchio.how_many() == 0

    def test(self):
        @accrocchio
        def d(a, b):
            pass

        self.assertEqual(0, accrocchio.how_many())
        [d(1, 2) for _ in range(3)]
        self.assertEqual(3, accrocchio.how_many())
        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())

    def test_observers(self):
        @accrocchio
        def d(a, b):
            pass

        observer = mock.create_autospec(AccrocchioObserver)
        observers.add_accrocchio_observer(observer)
        d(1, 2)
        self.assertEqual(0, observer.reset.call_count)
        self.assertEqual(1, observer.on_accrocchio.call_count)
        d(1, 2)
        self.assertEqual(0, observer.reset.call_count)
        self.assertEqual(2, observer.on_accrocchio.call_count)
        accrocchio.reset()
        self.assertEqual(1, observer.reset.call_count)

    def test_metaclass(self):
        class Dino(metaclass=Accrocchio):
            def __init__(self, xxxxx, y=32):
                pass

            def a(self):
                return 666

        self.assertEqual(1, accrocchio.how_many())
        Dino(1, y=10)
        self.assertEqual(2, accrocchio.how_many())
