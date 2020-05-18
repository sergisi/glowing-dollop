import unittest
import src.simulator as sim


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.person = 10
        self.ring_order = 4
        self.messages_list = [1, 3, 4]

    def test_raise_exception_simulation(self):
        with self.assertRaises(ValueError):
            sim.simulation_first(10, 11, [3])
        with self.assertRaises(ValueError):
            sim.simulation(10, 11, [3])

    def test_simulation_first(self):
        for person, mset in zip(self.messages_list,
                                sim.simulation_first(self.person, self.ring_order, self.messages_list)):
            self.assertIn(person, mset)

    def test_simulation(self):
        for person, mset in zip(self.messages_list,
                                sim.simulation(self.person, self.ring_order, self.messages_list)):
            self.assertIn(person, mset)

    def test_ring_order_in_choices(self):
        or_weights = [20, 30, 40, 20]
        weights = or_weights.copy()
        for i in range(len(weights)):
            wlen = i + 1
            print("=====", wlen)
            print(weights)
            self.assertEqual(len(sim.get_choices(weights, wlen)), wlen, f'{len(sim.get_choices(weights, wlen))} {wlen}')
            weights = or_weights.copy()
