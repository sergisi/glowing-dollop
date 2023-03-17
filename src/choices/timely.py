"""
# Timely preferential attachment
The idea is to grab the last n messages, instead of all the history. I think this will prevent snowballing
effect to a certain degree, and if the user behaviour changes, then at n messages it will adapt correctly.
"""

import dataclasses as dto
import random
from .choice import Choice
from .weighted_choice import *
from ..context import Context


class Weight:
    def __init__(self, people, n):
        self._weights = [0 for _ in range(people)]
        self.message_queue = [None for _ in range(n)]
        self.curr = 0

    def push(self, sign: list[int]):
        if self.message_queue[self.curr] is not None:
            for pid in self.message_queue[self.curr]:
                self._weights[pid] -= 1
        for pid in sign:
            self._weights[pid] += 1
        self.message_queue[self.curr] = sign
        self.curr = (self.curr + 1) % len(self.message_queue)

    def __getitem__(self, instance):
        return self.weights[instance]

    def weights(self, initial_weight, weight):
        return [initial_weight + weight * i for i in self._weights]

    def __repr__(self):
        return f"Weight({self.weights=}, {self.message_queue=}, {self.curr=})"


def timely_attachment_choice(
    message_weight: int,
    initial_weight: int,
    memory: int,
) -> Choice:
    def a(context: Context, message_list: list[int]):
        weights = Weight(context.people, memory)
        result = []
        for msg in message_list:
            w = weights.weights(initial_weight, message_weight)
            # User that sends the message is of course in the group, so don't add it two times.
            w[msg] = 0
            actual = get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            weights.push(actual)
        return result

    return a


def randomly_attachment_choice(
    memory: int,
) -> Choice:
    def a(context: Context, message_list: list[int]):
        weights = Weight(context.people, memory)
        result = []
        for msg in message_list:
            w = weights.weights(random.randint(1, 5), random.randint(1, 10))
            # User that sends the message is of course in the group, so don't add it two times.
            w[msg] = 0
            actual = get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            weights.push(actual)
        return result

    return a
