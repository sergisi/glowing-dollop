from .preferential import *
from .timely import *


def uniform_simulator(context: Context, msg_list: list[int]) -> list[list[int]]:
    """
    Takes a random number of k elements in order to sign the message.
    :return: list of group encrypted messages
    """
    result = []
    choices = list(range(context.people))
    for msg in msg_list:
        actual = random.sample(choices, k=context.ring_order)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
    return result
