import unittest
from src.choices import *
from src.context import Context


class ChoiceTest(unittest.TestCase):
    ctx: Context

    def setUp(self):
        self.ctx = Context(10, 4, lambda _: list(range(10)) + list(range(5)))

    def check(self, sigs):
        for e, s in zip(self.ctx.message_list, sigs):
            self.assertIn(e, s)
        self.assertTrue(len(self.ctx.message_list), len(sigs))

    def test_uniform(self):
        self.check(uniform_simulator(self.ctx, self.ctx.message_list))

    def test_zipf(self):
        signatures = preferential_attachment_choice(3, 1)(self.ctx, self.ctx.message_list)
        self.check(signatures)

class TimelyWeightTest(unittest.TestCase):

    def test_weight(self):
        w = Weight(5, 3, 1, 3)
        w.push([0, 1, 2, 3])
        self.assertEqual([4, 4, 4, 4, 1], w.weights)
        # assertions
        w.push([0, 1, 3, 4])
        self.assertEqual([7, 7, 4, 7, 4], w.weights)
        w.push([0, 1, 2, 4])
        self.assertEqual([10, 10, 7, 7, 7], w.weights)
        w.push([1, 2, 3, 4])
        self.assertEqual([7, 10, 7, 7, 10], w.weights)
        self.assertEqual(10, w[1])
        self.assertEqual(7, w[0])
