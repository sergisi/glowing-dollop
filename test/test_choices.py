import unittest
from src.choices import UniformSim, PreferentialAttachmentSim
from abc import ABC


class TemplateTest(unittest.TestCase, ABC):

    def setUp(self):
        self.persons = 10
        self.ring_order = 4
        self.message_list = list(range(10)) + list(range(5))
        self.choice = None

    def check(self):
        sigs = self.choice.apply()
        for e, s in zip(self.message_list, sigs):
            self.assertIn(e, s)
        self.assertTrue(len(self.message_list), len(sigs))


class UniformTest(TemplateTest):

    def setUp(self):
        super().setUp()
        self.choice = UniformSim(self.persons, self.ring_order, self.message_list)

    def test(self):
        self.check()


class PreferentialAttachmentTest(TemplateTest):

    def setUp(self):
        super().setUp()
        self.choice = PreferentialAttachmentSim(self.persons, self.ring_order, self.message_list)

    def test(self):
        self.check()
