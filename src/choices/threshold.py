import random
from typing import List

from .choice import Choice
from .preferential import _accumulate_weights


class ThresholdSim(Choice):

    def __init__(self, people: int, ring_order: int, message_list: List[int], message_weight: int = 100):
        super().__init__(people, ring_order, message_list)
        self.signatures = [0] * self.people
        self.author_msgs = [0] * self.people
        from src.analysis.anonymity import calculate
        self.message_weight = message_weight
        self.threshold = calculate(len(message_list), ring_order, people)

    def is_under_threshold(self, i):
        return (self.signatures[i] / max(self.author_msgs[i], 1)) <= self.threshold

    def _find_ball(self, r, accw):
        for i, w in enumerate(accw):
            if r < w:
                if self.is_under_threshold(i):
                    return i
                else:
                    return None

    def _get_elem(self, weights) -> int:
        """
            Then choses a random number between [0, 4),
            as for is the last number. Then gets the most left
            number that the random number generated is smaller.
        """
        accw = _accumulate_weights(weights)
        r = None
        while r is None:
            r = random.randint(0, accw[-1] - 1)
            r = self._find_ball(r, accw)
        return r

    def _get_subset_pool(self, weights: List[int], k: int) -> List[int]:
        """
            This number is set to 0 and added to the results
            and so on.
            :param weights -> List[int]: a list containing the weight of
                the nth member, as how many messages
                has been posted using its name.
            :param k: number of people to be taken
            :return List[int]: list of the people choosed.
        """
        res = []
        for _ in range(k):
            n = self._get_elem(weights)
            while n in res:
                n = self._get_elem(weights)
            res.append(n)
            self.signatures[n] += 1
        return res

    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * self.people
        for msg in self.message_list:
            w = list(weights)
            w[msg] = 0
            self.author_msgs[msg] += 1
            actual = self._get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += self.message_weight
        return result
