import random
from typing import List

from .choice import Choice


def _accumulate_weights(weigth_list) -> List[int]:
    """
    Gets a weighted list choice given a list of weights
        and a number to be taken.
        The list does not contain any repeated members. The algorithm
        tranfroms the list in a accomulated weights such as:
            [1, 2, 1, 0] -> [1, 3, 4, 4]
    """
    res = []
    acc = 0
    for i in weigth_list:
        acc += i
        res.append(acc)
    return res


def _get_elem(weights) -> int:
    """
        Then choses a random number between [0, 4),
        as for is the last number. Then gets the most left
        number that the random number generated is smaller.
    """
    accw = _accumulate_weights(weights)
    r = random.randint(0, accw[-1] - 1)
    for i, w in enumerate(accw):
        if r < w:
            return i
    raise ValueError


def _get_subset_pool(weights: List[int], k: int) -> List[int]:
    """
        This number is set to 0 and added to the results
        and so on.
        :param weights -> List[int]: a list containing the weight of
            the nth member, as how many messages
            has been posted using its name.
        :param k -> int : number of people to be taken
        :return List[int]: list of the people choosed.
    """
    res = []
    for _ in range(k):
        n = _get_elem(weights)
        while n in res:
            n = _get_elem(weights)
        res.append(n)
    return res


class PreferentialAttachmentSim(Choice):

    def __init__(self, people: int, ring_order: int, message_list: List[int], message_weight: int, initial_weight):
        super().__init__(people, ring_order, message_list)
        self.message_weight = message_weight
        self.weights = [initial_weight] * self.people

    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        for msg in self.message_list:
            w = list(self.weights)
            w[msg] = 0
            actual = _get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                self.weights[i] += self.message_weight
        return result


class UniquePAttachSim(PreferentialAttachmentSim):

    def __init__(self, people: int, ring_order: int, message_list: List[int], message_weight: int):
        super().__init__(people, ring_order, message_list, message_weight, 1)

    def apply(self) -> List[List[int]]:
        result = []
        self.weights = [1] * self.people
        for msg in self.message_list:
            w = list(self.weights)
            w[msg] = 0
            current_signature = _get_subset_pool(w, self.ring_order - 1)
            current_signature.append(msg)
            self.weights[msg] += self.message_weight
            result.append(current_signature)
        return result


class IncWeightPASim(Choice):

    def __init__(self, people: int, ring_order: int, message_list: List[int], min_weight: int, max_weight: int,
                 p: int):
        super().__init__(people, ring_order, message_list)
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.p = p

    def weights_values(self):
        p = [0] * len(self.message_list)
        for i, w in enumerate(range(self.min_weight, self.max_weight + 1)):
            p[i] += ((1 - self.p) ** i) * self.p
        total = sum(p)
        quantity = list(map(int, map(lambda x: x / total * len(self.message_list), p)))
        while sum(quantity) < len(self.message_list):
            quantity[0] += 1
        res = []
        for w, q in zip(range(self.min_weight, self.max_weight + 1), quantity):
            res += [w] * q
        return res

    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * self.people
        message_weights = self.weights_values()
        for i, msg in enumerate(self.message_list):
            w = list(weights)
            w[msg] = 0
            actual = _get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += message_weights[i]
        return result
