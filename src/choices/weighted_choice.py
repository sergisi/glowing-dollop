"""
Module that contains functions to take a choice given a list of weights.

The idea is that of a colored bag of balls. More explained, every point
in the list has a number of balls. So for exemple [20, 30, 5] means that
there are 20 balls of red, 30 of green and 5 of blue. This module simualtes
which color is chosed randomly in this problem. The values v must conform
$v \geq 0$.

The algorithm could get an improvement in efficiency using a dicatomic search
in get_elem, as the list is ordered.
"""
import random


def accumulate_weights(weigth_list: list[int]) -> list[int]:
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


def get_elem(accw: list[int]) -> int:
    """
    Given a weighted list of identifications, choose one according to its weight.

    The way to do so: every position has the accumulated weight. That's: the
    weight that it has plus the weight of the previous one. This means that if
    it is the sum of all the weights possible, then all of them have a
    probability of w/s to be chosen. Note that if a weight is 0, then it's not
    possible to be chosen.

    Further improvement could be done with a dicatomic search.

    :param accw -> list[int]: accumlated list of weights
    """
    r = random.randint(0, accw[-1] - 1)
    for i, w in enumerate(accw):
        if r < w:
            return i
    raise ValueError(f"Impossible state: {r} > {accw[-1]}")


def get_subset_pool(weights: list[int], k: int) -> list[int]:
    """
    Choses a group message randomly weighted, aka. preferential attachment.
    :param weights -> list[int]: a list containing the weight of
        the nth member, as how many messages
        has been posted using its name.
    :param k -> int : number of people to be taken
    :return list[int]: list of the people choosed.
    """
    res = []
    accw = accumulate_weights(weights)
    for _ in range(k):
        n = get_elem(accw)
        while n in res:
            n = get_elem(accw)
        res.append(n)
    return res
