import unittest

from src.data import Context, UniformContext
from src.distribution import Distribution, UniformDistribution
from functools import reduce

from src.simulation import Simulation


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.people = 10
        self.ring_order = 4
        self.context: Context = UniformContext(self.people, self.ring_order)
        self.distribution = self.context.distribution()

    def test_simulation_first(self):
        pass

    def test_simulation(self):
        simulation = Simulation(self.context)
        signs = simulation.simulate()
        for i in range(self.people):
            self.assertIn(i, reduce(set.union, map(set, signs)))
        for i, p in enumerate(simulation.msg_list):
            self.assertIn(p, signs[i])
