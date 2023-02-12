import random
import typing
from ..context import context

Choice = typing.Function[[Context], list[list[int]]]

def _accumulate_weights(weigth_list: list[int]) -> list[int]:
    """
    Gets a weighted list choice given a list of weights
        and a number to be taken.
        The list does not contain any repeated members. The algorithm
        tranfroms the list in a accomulated weights such as:
            [1, 2, 1, 0] -> [1, 3, 4, 4]
    """
    res = []
    acc = 0
    for i in weigth_list:
        acc += i
        res.append(acc)
    return res


def _get_elem(accw: list[int]) -> int:
    """
    Given a weighted list of identifications, choose one according to its weight.

    The way to do so: every position has the accumulated weight. That's: the weight that it has
    plus the weight of the previous one. This means that if s is the sum of all the weights possible,
    then all of them have a probability of w/s to be chosen. Note that if a weight is 0, then it's not
    possible to be chosen.

    :param accw -> list[int]: accumlated list of weights
    """
    r = random.randint(0, accw[-1] - 1)
    for i, w in enumerate(accw):
        if r < w:
            return i
    raise ValueError(f'Impossible state: {r} > {accw[-1]}')


def _get_subset_pool(weights: list[int], k: int) -> list[int]:
    """
    Choses a group message randomly weighted, aka. preferential attachment.
    :param weights -> list[int]: a list containing the weight of
        the nth member, as how many messages
        has been posted using its name.
    :param k -> int : number of people to be taken
    :return list[int]: list of the people choosed.
    """
    res = []
    accw = _accumulate_weights(weights)
    for _ in range(k):
        n = _get_elem(accw)
        while n in res:
            n = _get_elem(accw)
        res.append(n)
    return res

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
            actual = _get_subset_pool(w, ring_order - 1)
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
            actual = _get_subset_pool(w, context.ring_order - 1)
            actual.append(msg)
            result.append(actual)
            for i in actual:
                weights[i] += message_weights[i]
        return result

