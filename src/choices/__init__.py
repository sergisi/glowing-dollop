from __future__ import annotations
from abc import ABC, abstractmethod
import random
from typing import List


class Choice(ABC):

    def __init__(self, persons: int, ring_order: int,
                 message_list: List[int]):
        if ring_order > persons:
            raise ValueError
        self.persons = persons
        self.ring_order = ring_order
        self.message_list = message_list

    @abstractmethod
    def apply(self) -> List[List[int]]:
        pass


class UniformSim(Choice):

    def apply(self) -> List[List[int]]:
        """
        Takes a random number of k elements in order to sign the message.
        :return:
        """
        result = []
        choices = {i for i in range(self.persons)}
        for msg in self.message_list:
            actual = random.sample(choices, k=self.ring_order)
            if msg not in actual:
                actual[0] = msg
            result.append(actual)
        return result


class PreferentialAttachmentSim(Choice):

    def __init__(self, persons: int, ring_order: int, message_list: List[int], message_weight: int = 100):
        super().__init__(persons, ring_order, message_list)
        self.message_weight = message_weight

    def _accumulate_weights(self, weigth_list) -> List[int]:
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

    def _get_elem(self, weights) -> int:
        """
            Then choses a random number between [0, 4),
            as for is the last number. Then gets the most left
            number that the random number generated is smaller.
        """
        accw = self._accumulate_weights(weights)
        r = random.randint(0, accw[-1] - 1)
        for i, w in enumerate(accw):
            if r < w:
                return i
        raise ValueError

    def _get_subset_pool(self, weights: List[int], k: int) -> List[int]:
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
            n = self._get_elem(weights)
            res.append(n)
            weights[n] = 0
        return res

    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * self.persons
        for msg in self.message_list:
            w = list(weights)
            w[msg] = 0
            actual = self._get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += self.message_weight
        return result


class UniquePAttachSim(Choice):

    def __init__(self, persons: int, ring_order: int, message_list: List[int], message_weight: int):
        super().__init__(persons, ring_order, message_list)
        self.weight_cost = message_weight
        self.weights = None

    def _accumulate_weights(self, weigth_list) -> List[int]:
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

    def _get_elem(self, weights) -> int:
        """
            Then choses a random number between [0, 4),
            as for is the last number. Then gets the most left
            number that the random number generated is smaller.
        """
        accw = self._accumulate_weights(weights)
        r = random.randint(0, accw[-1] - 1)
        for i, w in enumerate(accw):
            if r < w:
                return i
        raise ValueError

    def _get_subset_pool(self, weights: List[int], k: int) -> List[int]:
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
            n = self._get_elem(weights)
            res.append(n)
            weights[n] = 0
        return res

    def apply(self) -> List[List[int]]:
        result = []
        self.weights = [1] * self.persons
        self.generated = [0] * self.persons
        for msg in self.message_list:
            w = list(self.weights)
            w[msg] = 0
            self.generated[msg] += 1
            current_signature = self._get_subset_pool(w, self.ring_order - 1)
            current_signature.append(msg)
            self.weights[msg] += self.weight_cost
            result.append(current_signature)
            # for i in current_signature:
            #    self.weights[i] += self.weight_cost
        return result

class ThresholdSim(Choice):

    def __init__(self, persons: int, ring_order: int, message_list: List[int], message_weight: int = 100):
        super().__init__(persons, ring_order, message_list)
        from src.anonymity import calculate
        self.message_weight = message_weight
        self.threshold = calculate(len(message_list), ring_order, persons)

    def _accumulate_weights(self, weigth_list) -> List[int]:
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

    def is_under_threshold(self, i):
        return (self.signatures[i] / max(self.author_msgs[i], 1)) <= (self.threshold)       
            
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
        accw = self._accumulate_weights(weights)
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
            :param k -> int : number of people to be taken
            :return List[int]: list of the people choosed.
        """
        res = []
        for _ in range(k):
            n = self._get_elem(weights)
            res.append(n)
            self.signatures[n] += 1
            weights[n] = 0
        return res

    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * self.persons
        self.author_msgs = [0] * self.persons
        self.signatures = [0] * self.persons
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


class IncWeightPASim(Choice):

    def __init__(self, persons: int, ring_order: int, message_list: List[int], min_weight: int, max_weight: int, p: int):
        super().__init__(persons, ring_order, message_list)
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.p = p

    def _accumulate_weights(self, weigth_list) -> List[int]:
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

    def _get_elem(self, weights) -> int:
        """
            Then choses a random number between [0, 4),
            as for is the last number. Then gets the most left
            number that the random number generated is smaller.
        """
        accw = self._accumulate_weights(weights)
        r = random.randint(0, accw[-1] - 1)
        for i, w in enumerate(accw):
            if r < w:
                return i
        raise ValueError

    def _get_subset_pool(self, weights: List[int], k: int) -> List[int]:
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
            n = self._get_elem(weights)
            res.append(n)
            weights[n] = 0
        return res

    def weights_values(self):
        p = [0] * (self.max_weight - self.min_weight + 1)
        for i, w in enumerate(range(self.min_weight, self.max_weight+1)):
            p[i] += ((1 - self.p) ** i) * self.p
        total = sum(p)
        quantity = list(map(int, map(lambda x: x / total * len(self.message_list), p)))
        while sum(quantity) < len(self.message_list):
            quantity[0] += 1
        res = []
        for w, q in zip(range(self.min_weight, self.max_weight +1), quantity):
            res += [w] * q
        return res


    def apply(self) -> List[List[int]]:
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * self.persons
        message_weights = self.weights_values()
        for i, msg in enumerate(self.message_list):
            w = list(weights)
            w[msg] = 0
            actual = self._get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += message_weights[i]
        return result