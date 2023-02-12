from .preferential import *
from .threshold import ThresholdSim

def uniform_simulator(context: Context, msg_list: list[int]) -> list[list[int]]:
    """
    Takes a random number of k elements in order to sign the message.
    :return: list of group encrypted messages
    """
    result = []
    choices = {i for i in range(context.people)}
    for msg in msg_list:
        actual = random.sample(choices, k=context.ring_order)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
    return result
