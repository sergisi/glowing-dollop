from typing import List, Dict, Set, DefaultDict
from collections import defaultdict
import itertools
import operator
import random


def simulation_first(persons: int, ring_order: int, message_list: List[int]) -> List[List[int]]:
    """
        Simulates the forum aproach without using a weighted choice, instead is using a
        uniform approach.
        :param persons -> int: the number of people in the forum. Every person is named as [0, persons)
        :param ring_order -> int: the number of people to be selected in a post
        :param message_list -> List[int] : List of messages in order. For example [0, 3, 2]
            would send first "0" message, "3" message and "2" message
        :return List[List[int]] : A list of every set of people selected for the message. For
            example, in the first message could have been [3, 4, 0] as the people selected. All
            the results are appended in a message like [[3, 4, 0]...]. It's returned as a List of
            Lists instead of a List of Sets for performance.
    """
    if ring_order > persons:
        raise Exception
    result = []
    choices = {i for i in range(persons)}
    for msg in message_list:
        actual = random.sample(choices, k=ring_order)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
    return result


def get_choices(weights: List[int], k: int) -> List[int]:
    """
        Gets a weighted list choice given a list of weights and a number to be taken.
        The list does not contain any repeated members.
        The algorithm tranfroms the list in a accomulated weights such as [1, 2, 1, 0] -> [1, 3, 4, 4]
        Then choses a random number between [0, 4), as for is the last number. Then gets the most left
        number that the random number generated is smaller. This number is set to 0 and added to the results
        and so on.
        :param weights -> List[int]: a list containing the weight of the nth member, as how many messages
            has been posted using its name.
        :param k -> int : number of people to be taken
        :return List[int]: list of the people choosed.
    """

    def accomulate_weights(ls):
        res = []
        acc = 0
        for i in ls:
            acc += i
            res.append(acc)
        return res

    def get_next(w):
        accw = accomulate_weights(w)
        r = random.randint(0, accw[-1] - 1)
        for i, w in enumerate(accw):
            if r < w:
                return i

    res = []
    for _ in range(k):
        n = get_next(weights)
        res.append(n)
        weights[n] = 0
    return res


def simulation(persons: int, ring_order: int, message_list: List[int]) -> List[List[int]]:
    """
        Simulates the forum aproach using a weighted choice
        :param persons -> int: the number of people in the forum. Every person is named as [0, persons)
        :param ring_order -> int: the number of people to be selected in a post
        :param message_list -> List[int] : List of messages in order. For example [0, 3, 2]
            would send first "0" message, "3" message and "2" message
        :return List[List[int]] : A list of every set of people selected for the message. For
            example, in the first message could have been [3, 4, 0] as the people selected. All
            the results are appended in a message like [[3, 4, 0]...]. It's returned as a List of
            Lists instead of a List of Sets for performance.
    """
    if ring_order > persons:
        raise Exception
    result = []
    weights = [1] * persons
    for msg in message_list:
        w = list(weights)
        w[msg] = 0
        actual = get_choices(w, ring_order - 1)
        actual.append(msg)
        result.append(actual)
        for i in actual:
            weights[i] += 1
    return result


def simulation_to_dictionary(persons: int, simulation: List[List[int]]) -> List[int]:
    """
    Parses a result of a simulations to a List of integers, where the nth position is the 
    number of messages that this person has signed.
    :param persons -> int : number of persons in the simulation
    :param simulation -> List[List[int]] : result of a simulation
    :return List[int] : the nth position is the number of messages that the nth persone has signed
    """
    res = [0] * persons
    for ls in simulation:
        for person in ls:
            res[person] += 1
    return res


def probability_of_all(persons: int, message_list: List[int], simulation: List[List[int]]) -> List[float]:
    """
        Parses a simulation into a List containing in the nth value the anounimosity of the nth person.
        The common practice should be:
            def a(persons, k, message_list):
                sim = simulation(persons, k, message_list)
                return probability_of_all(persons, message_list, sim)
        But this way is more flexible (you can study the way that the numbers are choosen as you
        already have the simulation, for example)
        :param persons -> int : number of persons in the simulation.
        :param message_list -> List[int]: list of messages used in the simulation.
        :param simulation -> List[List[int]]: result of the simulation.
        :return List[int]: Returns a list of floating numbers where the nth position has that level of
        anounimosity.
    """
    sim = simulation_to_dictionary(persons, simulation)
    msgcount = [0] * persons
    for i in message_list:
        msgcount[i] += 1
    res = []
    for i in filter(lambda x: msgcount[x] != 0, range(persons)):
        res.append(sim[i] / msgcount[i])
    return res
