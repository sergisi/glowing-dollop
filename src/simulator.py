from typing import List, Dict
from collections import defaultdict
import random


def simulation_first(persons: int, ring_order: int, message_list: List[int]) -> List[List[int]]:
    result = []
    choices = {i for i in range(persons)}
    for msg in message_list:
        actual = random.sample(choices, k=ring_order - 1)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
    return result


def simulation(persons: int, ring_order: int, message_list: List[int]) -> List[List[int]]:
    result = []
    choices = [i for i in range(persons)]
    for msg in message_list:
        actual = random.sample(choices, k=ring_order)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
        choices.extend(actual)
    return result


def simulation_to_dictionary(persons: int, simulation: List[List[int]]) -> Dict[int, List[int]]:
    res = [[]] * persons
    for i, ls in enumerate(simulation):
        for person in ls:
            res[person].append(i)
    return res


def probability_of_all(persons: int, message_list: List[int], simulation: List[List[int]]):
    sim = simulation_to_dictionary(persons, simulation)
    msgcount = [0] * persons
    for i in message_list:
        msgcount[i] += 1
    res = []
    for i in range(persons):
        res.append(msgcount[i] / len(sim[i]))
    return res


