from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.choices import Choice
from src.distribution import Distributioner, UniformDistribution, MessageProducer
from src.distribution import Zipf


class Context(Distributioner, MessageProducer, ABC):

    def __init__(self, people: int, k: int):
        self._people = people
        self.__k = k
        self.msgs = None
        self.sc = None
        self.dis = None

    @abstractmethod
    def choice(self, msg_list) -> Choice:
        pass

    def get_people(self):
        return self._people

    def get_k(self):
        return self.__k

    def scorer(self):
        if self.sc is None:
            from src.analysis import AnonymityScorer
            self.sc = AnonymityScorer(self._people)
        return self.sc

    def messages(self) -> List[int]:
        if self.msgs is None:
            self.msgs = self.distribution().messages()
        return self.msgs


class UniformContext(Context):

    def choice(self, msg_list) -> Choice:
        from src.choices.uniform import UniformSim
        return UniformSim(self.get_people(), self.get_k(), msg_list)

    def distribution(self) -> UniformDistribution:
        if self.dis is None:
            self.dis =  UniformDistribution(self._people)
        return self.dis

    def __init__(self, people: int, k: int):
        super().__init__(people, k)


class ZipfContext(Context, ABC):
    def __init__(self, people: int, k: int, max_msg: int, s: float):
        super().__init__(people, k)
        self.__max_msg = max_msg
        self.__s = s

    def distribution(self) -> Zipf:
        if self.dis is None:
            self.dis = Zipf(self._people, self.__max_msg, self.__s)
        return self.dis
    
    def get_s(self):
        return self.__s
    
    def get_max_msg(self):
        return self.__max_msg

class UniformZipfContext(ZipfContext):

    def choice(self, msg_list) -> Choice:
        from src.choices.uniform import UniformSim
        return UniformSim(self.get_people(), self.get_k(), msg_list)


class PreferentialContext(ZipfContext):

    def choice(self, msg_list) -> Choice:
        from src.choices.preferential import PreferentialAttachmentSim as PASim
        return PASim(self.get_people(), self.get_k(), msg_list, self.get_weight(), self.get_initial_weight())

    def __init__(self, people: int, k: int, max_msg: int, s: float, initial_weight: int,
                 weight: int):
        super().__init__(people, k)
        self.__initial_weight = initial_weight
        self.__weight = weight

    def get_initial_weight(self):
        return self.__initial_weight

    def get_weight(self):
        return self.__weight

    def new_weight(self, new_weight: int) -> PreferentialContext:
        return PreferentialContext(self.get_people(), self.get_k(), self.__max_msg, self.__s,
                                   self.__initial_weight, new_weight)

    def new_initial_weight(self, new_init_weight: int) -> PreferentialContext:
        return PreferentialContext(self.get_people(), self.get_k(), self.__max_msg, self.__s,
                                   new_init_weight, self.__weight)
