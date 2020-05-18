import unittest
import src.simulator as sim


class MyTestCase(unittest.TestCase):

    def test_raise_exception_simulation(self):
        self.assertRaises(Exception, sim.simulation_first(10, 11, [3]))
        self.assertRaises(Exception, sim.simulation(10, 11, [3]))

