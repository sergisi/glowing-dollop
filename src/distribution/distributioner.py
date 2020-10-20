from abc import ABC, abstractmethod
from .distribution import Distribution


class Distributioner(ABC):

    @abstractmethod
    def distribution(self) -> Distribution:
        pass
