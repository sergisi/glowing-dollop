import random
import typing
from ..context import Context
from .choice import Choice
from .utils import *

def preferential_attachment_choice(
        message_weight: int,
        initial_weight: int,
        ) -> Choice:
    def a(context: Context, message_list: list[int]):
        weights = [initial_weight] * context.people
        result = []
        for msg in message_list:
            w = list(weights)
            # User that sends the message is of course in the group, so don't add it two times.
            w[msg] = 0
            actual = get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += message_weight
        return result
    return a

def unique_pattach(message_weight: int) -> Choice:
    return preferential_attachment_choice(message_weight, 1)


def _weights_values(context: Context, message_list):
    p = [0] * len(message_list)
    for i, w in enumerate(range(min_weight, max_weight + 1)):
        p[i] += ((1 - prob) ** i) * prob
    total = sum(p)
    quantity = list(map(int, map(lambda x: x / total * len(message_list), p)))
    while sum(quantity) < len(message_list):
        quantity[0] += 1
    res = []
    for w, q in zip(range(min_weight, max_weight + 1), quantity):
        res += [w] * q
    return res


def inc_weight_pas(
        min_weight: int,
        max_weight: int,
        prob: int
) -> Choice:
    """
    No idea what is this simulation.
    """
    def a(context: Context, message_list: list[int]):
        """
        For every message in the list, puts the list of the weights at 0
        :return:
        """
        result = []
        weights = [1] * context.people
        message_weights = weights_values(context, message_list)
        for i, msg in enumerate(message_list):
            w = list(weights)
            w[msg] = 0
            actual = get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += message_weights[i]
        return result

