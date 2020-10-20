from __future__ import annotations
from typing import List
from abc import ABC, abstractmethod

from src.choices import Choice
from src.distribution import Distributioner, Zipf, UniformDistribution
from src.distribution import Zipf


class Context(Distributioner, ABC):

    def __init__(self, people: int, k: int):
        self._people = people
        self.__k = k

    @abstractmethod
    def choice(self, msg_list) -> Choice:
        pass

    def get_people(self):
        return self._people

    def get_k(self):
        return self.__k


class UniformContext(Context):

    def choice(self, msg_list) -> Choice:
        from src.choices.uniform import UniformSim
        return UniformSim(self._people, self.__k, msg_list)

    def distribution(self) -> UniformDistribution:
        return UniformDistribution(self._people)

    def __init__(self, people: int, k: int):
        super().__init__(people, k)


class PreferentialContext(Context):

    def choice(self, msg_list) -> Choice:
        from src.choices.preferential import PreferentialAttachmentSim as PASim
        return PASim(self._people, self.__k, msg_list, self.__weight, self.__initial_weight)

    def distribution(self) -> Zipf:
        return Zipf(self._people, self.__max_msg, self.__s)

    def __init__(self, people: int, k: int, max_msg: int, s: float, initial_weight: int,
                 weight: int):
        super().__init__(people, k)
        self.__max_msg = max_msg
        self.__initial_weight = initial_weight
        self.__weight = weight
        self.__s = s

    def get_max_msg(self):
        return self.__max_msg

    def get_initial_weight(self):
        return self.__initial_weight

    def get_weight(self):
        return self.__weight

    def get_s(self):
        return self.__s

    def new_weight(self, new_weight: int) -> PreferentialContext:
        return PreferentialContext(self.get_people(), self.get_k(), self.__max_msg, self.__s,
                                   self.__initial_weight, new_weight)

    def new_initial_weight(self, new_init_weight: int) -> PreferentialContext:
        return PreferentialContext(self.get_people(), self.get_k(), self.__max_msg, self.__s,
                                   new_init_weight, self.__weight)
