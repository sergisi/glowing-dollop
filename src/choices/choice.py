from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Choice(ABC):

    def __init__(self, people: int, ring_order: int,
                 message_list: List[int]):
        if ring_order > people:
            raise ValueError
        self.people = people
        self.ring_order = ring_order
        self.message_list = message_list

    @abstractmethod
    def apply(self) -> List[List[int]]:
        pass
