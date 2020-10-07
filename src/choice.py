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
    def apply(self):
        pass


class UniformSim(Choice):

    def apply(self):
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

    def __accomulate_weights(self, weigth_list) -> List[int]:
        res = []
        acc = 0
        for i in weigth_list:
            acc += i
            res.append(acc)
        return res

    def __get_elem(self, weights) -> int:
        accw = self.__accomulate_weights(weights)
        r = random.randint(0, accw[-1] - 1)
        for i, w in enumerate(accw):
            if r < w:
                return i
        raise ValueError

    def __get_subset_pool(self, weights: List[int], k: int) -> List[int]:
        """
            Gets a weighted list choice given a list of weights
            and a number to be taken.
            The list does not contain any repeated members. The algorithm
            tranfroms the list in a accomulated weights such as:
                [1, 2, 1, 0] -> [1, 3, 4, 4]
            Then choses a random number between [0, 4),
            as for is the last number. Then gets the most left
            number that the random number generated is smaller.
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
            n = self.__get_elem(weights)
            res.append(n)
            weights[n] = 0
        return res

    def apply(self):
        result = []
        weights = [1] * self.persons
        for msg in self.message_list:
            w = list(weights)
            w[msg] = 0
            actual = self.__get_subset_pool(w, self.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += self.message_weight
        return result


if __name__ == "__main__":
    sim = PreferentialAttachmentSim(40, 4, [1, 2, 3])
    print(sim.apply())


class AbstractFactoryChoice:

    @staticmethod
    def AFUniform(persons: int, ring_order: int, message_list: List[int]):
        return UniformSim(persons, ring_order, message_list)

    @staticmethod
    def AFPAttach(persons: int, ring_order: int, message_list: List[int], weight: int):
        return PreferentialAttachmentSim(persons, ring_order, message_list, weight)


class ChoiceBuilder(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def set_message_list(self, message_list: List[int]):
        pass

    @abstractmethod
    def build(self) -> Choice:
        pass
    

class PAttachBuilder(ChoiceBuilder):

    def __init__(self):
        super().__init__()
        self.persons = None
        self.ring_order = None
        self.message_list = None
        self.weight = None


    def set_persons(self, persons) -> PAttachBuilder:
        if self.persons is None:
            self.persons = persons
            return self
        raise EnvironmentError
    
    def set_ring_order(self, ring_order: int) -> PAttachBuilder:
        if self.ring_order is None:
            self.ring_order = ring_order
            return self
        raise EnvironmentError

    def set_message_list(self, message_list: List[int]) -> PAttachBuilder:
        if self.message_list is None:
            self.message_list = message_list
            return self
        raise EnvironmentError

    def set_weight(self, weight) -> PAttachBuilder:
        if self.weight is None:
            self.weight = weight
            return self
        raise EnvironmentError

    def build(self):
        if self.persons is None or self.ring_order is None or self.message_list is None or self.weight is None:
            raise ValueError
        return PreferentialAttachmentSim(self.persons, self.ring_order, self.message_list, self.weight)