"""
# Timely preferential attachment
The idea is to grab the last n messages, instead of all the history. I think this will prevent snowballing
effect to a certain degree, and if the user behaviour changes, then at n messages it will adapt correctly.
"""

import dataclasses as dto
from .choice import Choice
from .utils import *
from ..context import Context

class Weight:

    def __init__(self, people, n, initial_weight, weight):
        self.weight = weight
        self.weights = [initial_weight for _ in range(people)]
        self.message_queue = [None for _ in range(n)]
        self.curr = 0


    def push(self, sign: list[int]):
        if self.message_queue[self.curr] is not None:
            for pid in self.message_queue[self.curr]:
                self.weights[pid] -= self.weight
        for pid in sign:
            self.weights[pid] += self.weight
        self.message_queue[self.curr] = sign
        self.curr = (self.curr + 1) % len(self.message_queue)

    def __getitem__(self, instance):
        return self.weights[instance]

    def __repr__(self):
        return f'Weight({self.weight=}, {self.weights=}, {self.message_queue=}, {self.curr=})'


def timely_attachment_choice(
        message_weight: int,
        initial_weight: int,
        memory: int,
) -> Choice:
    def a(context: Context, message_list: list[int]):
        weights = Weight(context.people, memory, initial_weight, message_weight)
        result = []
        for msg in message_list:
            w = list(weights.weights)
            # User that sends the message is of course in the group, so don't add it two times.
            w[msg] = 0
            actual = get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            weights.push(actual)
        return result
    return a
