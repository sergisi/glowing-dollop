import unittest
from src.distribution import *
from src.context import Context


class ZipfTest(unittest.TestCase):

    def setUp(self):
        self.people = 200
        self.ring_order = 5

    def test_uniform_distribution(self):
        ctx = Context(self.people, self.ring_order, uniform_distribution)
        self.assertEqual(list(range(self.people)), ctx.message_list)


    def test_correct_msm(self):
        num_persons = 30
        s = 2.5
        maximum_messages = 4

        def prob_msm(x): return 1 / (x ** s)

        total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
        number_persons = [prob_msm(x) * num_persons / total
                          for x in range(1, num_persons + 1)]
        c_number_persons = correct_msm(number_persons, num_persons)
        self.assertEqual(num_persons, sum(c_number_persons))

    def test_zipf(self):
        from collections import Counter
        num_persons = 30
        s = 2.5
        maximum_messages = 4
        ctx = Context(num_persons, self.ring_order, zipf_distribution(maximum_messages, s))
        prob_msm = lambda x: 1 / (x ** s)
        total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
        number_persons = [prob_msm(x) * num_persons / total
                          for x in range(1, num_persons + 1)]
        c_number_persons = correct_msm(number_persons, num_persons)
        persons = Counter(ctx.message_list).items()
        get_num_msgs = lambda x: lambda t: t[1] == x
        for i in range(maximum_messages):
            self.assertEqual(c_number_persons[i], len(list(filter(get_num_msgs(i + 1), persons))))


if __name__ == "__main__":
    unittest.main()
