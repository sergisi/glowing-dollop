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


class WeightAfterMessageTest(TemplateTest):

    def setUp(self):
        super().setUp()
        self.choice = PreferentialAttachmentSim(self.persons, self.ring_order, [0], 1, 1)

    def test(self):
        signatures = self.choice.apply()
        self.assertIn(0, signatures[0])
        for member in signatures[0]:
            self.assertEqual(2, self.choice.weights[member], f"The weight of the participant {member} is not 2")


class WeightAfter2MessagesAuthorTest(TemplateTest):

    def setUp(self):
        super().setUp()
        self.choice = PreferentialAttachmentSim(self.persons, self.ring_order, [0, 0], 1, 1)

    def test(self):
        signatures = self.choice.apply()
        for signature in signatures:
            self.assertIn(0, signature)
        self.assertEqual(3, self.choice.weights[0])


class WeightAfter2MessagesOthersTest(TemplateTest):

    def setUp(self):
        super().setUp()
        self.choice = PreferentialAttachmentSim(4, 4, [0, 0], 1, 1)

    def test(self):
        signatures = self.choice.apply()
        for p in range(0, 4):
            for signature in signatures:
                self.assertIn(p, signature, f"{p} is not in signature {signature}")
        for p in range(0, 4):
            self.assertEqual(3, self.choice.weights[p], f"It failed member {p}")
