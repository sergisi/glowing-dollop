from __future__ import annotations
from src.choices import Choice, UniformSim, PreferentialAttachmentSim, UniquePAttachSim
from typing import List
from abc import ABC, abstractmethod


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
    def set_persons(self, persons) -> PAttachBuilder:
        pass

    @abstractmethod
    def set_ring_order(self, ring_order: int) -> PAttachBuilder:
        pass

    @abstractmethod
    def set_message_list(self, message_list: List[int]):
        pass

    @abstractmethod
    def reset(self) -> ChoiceBuilder:
        pass

    @abstractmethod
    def build(self) -> Choice:
        pass


class UniformBuilder(ChoiceBuilder):

    def __init__(self):
        super().__init__()
        self.message_list = None
        self.persons = None
        self.ring_order = None

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

    def set_message_list(self, message_list: List[int]):
        if self.message_list is None:
            self.message_list = message_list
            return self
        raise EnvironmentError

    def reset(self):
        return UniformBuilder()

    def build(self) -> Choice:
        return UniformSim(self.persons, self.ring_order, self.message_list)


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

    def reset(self):
        return PAttachBuilder()

    def build(self):
        if self.persons is None or self.ring_order is None or self.message_list is None or self.weight is None:
            raise ValueError
        return PreferentialAttachmentSim(self.persons, self.ring_order, self.message_list, self.weight)


class UniquePAttachBuilder(ChoiceBuilder):

    def __init__(self):
        super().__init__()
        self.persons = None
        self.ring_order = None
        self.message_list = None
        self.weight = None

    def set_persons(self, persons) -> UniquePAttachBuilder:
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

    def reset(self):
        return UniquePAttachBuilder()

    def build(self):
        if self.persons is None or self.ring_order is None or self.message_list is None or self.weight is None:
            raise ValueError
        return UniquePAttachSim(self.persons, self.ring_order, self.message_list, self.weight)
