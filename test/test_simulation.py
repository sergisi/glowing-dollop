import unittest
from src.simulation import Simulation 
from src.choices.patterns import UniformBuilder
from src.distribution import Distribution, UniformDistribution
from functools import reduce

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.persons = 10
        self.ring_order = 4
        self.distribution = UniformDistribution(self.persons)
        self.simulation = Simulation(self.persons, self.ring_order, UniformBuilder())

    def test_simulation_first(self):
        pass

    def test_simulation(self):
        signs = self.simulation.simulate(self.distribution)
        for i in range(self.persons):
            self.assertIn(i , reduce(set.union, map(set, signs)))
"""
    def test_ring_order_in_choices(self):
        or_weights = [20, 30, 40, 20]
        weights = or_weights.copy()
        for i in range(len(weights)):
            wlen = i + 1
            self.assertEqual(len(sim.get_choices(weights, wlen)), wlen)
            weights = or_weights.copy()

    def test_get_message_count(self):
        persons = 8
        messages = [0] + 3 * [2] + [1] * 4 + 2 * [7] + [4] * 5
        self.assertEqual([1, 4, 3, 0, 5, 0, 0, 2], sim.get_messagecount(persons, messages))

    def test_simulation_to_dictionary(self):
        persons = 8
        simulation = [[1, 2, 3, 4], [0, 1, 3, 6], [7, 3, 4, 6]]
        self.assertEqual([1, 2, 1, 3, 2, 0, 2, 1], sim.simulation_to_dictionary(persons, simulation))

    def test_probability_of_all(self):
        persons = 8
        messages = [2, 3, 7]
        simulation = [[1, 2, 3, 4], [0, 1, 3, 6], [7, 3, 4, 6]]
        prob = sim.probability_of_all(persons, messages, simulation)
        for p in messages:
            self.assertNotEqual(0, prob[p])
        for nm in set(range(8)) - set(messages):
            self.assertEqual(0, prob[nm])
"""