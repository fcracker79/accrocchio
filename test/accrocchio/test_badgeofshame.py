import unittest
from unittest import mock

# noinspection PyUnresolvedReferences
from accrocchio.badgeofshame import accrocchio, detonator, epoxy, compromise, blinder, flypaper
from accrocchio.badgeofshame import this_is_a, this_is_an
from accrocchio.observers import AccrocchioObserver


class TestBadgeOfShame(unittest.TestCase):
    def setUp(self):
        accrocchio.reset()
        assert accrocchio.how_many() == 0

    def test(self):
        @accrocchio
        def accrocchio_fun(a, b):
            pass

        @detonator
        def detonator_fun(a, b):
            pass

        @epoxy
        def epoxy_fun(a, b):
            pass

        self.assertEqual(0, accrocchio.how_many())
        [accrocchio_fun(1, 2) for _ in range(3)]
        self.assertEqual(3, accrocchio.how_many())
        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        [accrocchio_fun(1, 2) for _ in range(3)]

        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        self.assertEqual(0, detonator.how_many())
        self.assertEqual(0, epoxy.how_many())
        [detonator_fun(1, 2) for _ in range(3)]
        [epoxy_fun(1, 2) for _ in range(4)]
        self.assertEqual(7, accrocchio.how_many())
        self.assertEqual(3, detonator.how_many())
        self.assertEqual(4, epoxy.how_many())
        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        self.assertEqual(0, detonator.how_many())  # We expect it to have detonators being reset as well
        self.assertEqual(0, epoxy.how_many())

        [detonator_fun(1, 2) for _ in range(3)]
        [epoxy_fun(1, 2) for _ in range(4)]
        epoxy.reset()
        self.assertEqual(7, accrocchio.how_many())
        self.assertEqual(3, detonator.how_many())
        self.assertEqual(0, epoxy.how_many())

    def test_observers(self):
        @accrocchio
        def accrocchio_fun(a, b):
            pass

        @detonator
        def detonator_fun(a, b):
            pass

        @flypaper
        def flypaper_fun(a, b):
            pass

        accrocchio_observer = mock.create_autospec(AccrocchioObserver)
        accrocchio.add_observer(accrocchio_observer)
        detonator_observer = mock.create_autospec(AccrocchioObserver)
        detonator.add_observer(detonator_observer)
        accrocchio_fun(1, 2)
        self.assertEqual(0, accrocchio_observer.reset.call_count)
        self.assertEqual(0, detonator_observer.on_accrocchio.call_count)
        self.assertEqual(1, accrocchio_observer.on_accrocchio.call_count)
        detonator_fun(1, 2)
        self.assertEqual(1, detonator_observer.on_accrocchio.call_count)
        self.assertEqual(0, accrocchio_observer.reset.call_count)
        self.assertEqual(2, accrocchio_observer.on_accrocchio.call_count)
        accrocchio_fun(1, 2)
        self.assertEqual(0, accrocchio_observer.reset.call_count)
        self.assertEqual(3, accrocchio_observer.on_accrocchio.call_count)
        accrocchio.reset()
        self.assertEqual(1, accrocchio_observer.reset.call_count)
        self.assertEqual(1, detonator_observer.reset.call_count)
        detonator.reset()
        self.assertEqual(1, accrocchio_observer.reset.call_count)
        self.assertEqual(2, detonator_observer.reset.call_count)

    def test_metaclass(self):
        class AccrocchioClass(metaclass=accrocchio):
            pass

        class CompromiseClass(metaclass=compromise):
            pass

        class BlinderClass(metaclass=blinder):
            pass

        self.assertEqual(3, accrocchio.how_many())
        self.assertEqual(1, compromise.how_many())
        self.assertEqual(1, blinder.how_many())
        self.assertEqual(0, epoxy.how_many())
        AccrocchioClass()
        self.assertEqual(4, accrocchio.how_many())
        self.assertEqual(1, compromise.how_many())
        self.assertEqual(1, blinder.how_many())
        self.assertEqual(0, epoxy.how_many())
        CompromiseClass()
        self.assertEqual(5, accrocchio.how_many())
        self.assertEqual(2, compromise.how_many())
        self.assertEqual(1, blinder.how_many())
        self.assertEqual(0, epoxy.how_many())

    def test_one_shot_accrocchi(self):
        self.assertEqual(0, accrocchio.how_many())
        [this_is_an(accrocchio) for _ in range(3)]
        self.assertEqual(3, accrocchio.how_many())
        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        [this_is_an(accrocchio) for _ in range(3)]

        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        self.assertEqual(0, detonator.how_many())
        self.assertEqual(0, epoxy.how_many())
        [this_is_a(detonator) for _ in range(3)]
        [this_is_an(epoxy) for _ in range(4)]
        self.assertEqual(7, accrocchio.how_many())
        self.assertEqual(3, detonator.how_many())
        self.assertEqual(4, epoxy.how_many())
        accrocchio.reset()
        self.assertEqual(0, accrocchio.how_many())
        self.assertEqual(0, detonator.how_many())  # We expect it to have detonators being reset as well
        self.assertEqual(0, epoxy.how_many())

        [this_is_a(detonator) for _ in range(3)]
        [this_is_an(epoxy) for _ in range(4)]
        epoxy.reset()
        self.assertEqual(7, accrocchio.how_many())
        self.assertEqual(3, detonator.how_many())
        self.assertEqual(0, epoxy.how_many())
