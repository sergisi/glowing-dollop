from __future__ import annotations

import random
from typing import List

from .choice import Choice


class UniformSim(Choice):
    def apply(self) -> List[List[int]]:
        """
        Takes a random number of k elements in order to sign the message.
        :return:
        """
        result = []
        choices = {i for i in range(self.people)}
        for msg in self.message_list:
            actual = random.sample(choices, k=self.ring_order)
            if msg not in actual:
                actual[0] = msg
            result.append(actual)
        return result
