import unittest
import src.zipf as zipf


class ZipfTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_zipf(self):
        from collections import Counter
        num_persons = 30
        s = 2.5
        maximum_messages = 4
        prob_msm = lambda x: 1 / (x ** s)
        total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
        number_persons = [prob_msm(x) * num_persons / total
                          for x in range(1, num_persons + 1)]
        c_number_persons = zipf.correct_msm(number_persons, num_persons)
        zipf_dist = zipf.zipf(num_persons, maximum_messages, s)
        persons = Counter(zipf_dist).items()
        get_num_msgs = lambda x: lambda t: t[1] == x
        for i in range(maximum_messages):
            self.assertEqual(c_number_persons[i], len(list(filter(get_num_msgs(i+1), persons))))


    def test_correct_msm(self):
        num_persons = 30
        s = 2.5
        maximum_messages = 4
        prob_msm = lambda x: 1 / (x ** s)
        total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
        number_persons = [prob_msm(x) * num_persons / total
                          for x in range(1, num_persons + 1)]
        c_number_persons = zipf.correct_msm(number_persons, num_persons)
        self.assertEqual(num_persons, sum(c_number_persons))
        self.assertEqual(0, num_persons[maximum_messages])
