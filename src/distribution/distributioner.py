from abc import ABC, abstractmethod
from typing import List

from .distribution import Distribution


class Distributioner(ABC):

    @abstractmethod
    def distribution(self) -> Distribution:
        pass


class MessageProducer(ABC):

    @abstractmethod
    def messages(self) -> List[int]:
        pass
