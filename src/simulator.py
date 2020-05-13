from typing import List, Dict, Set, DefaultDict
from collections import defaultdict
import itertools
import operator
import random

def simulation_first(persons: int, ring_order: int, message_list: List[int]) -> List[List[int]]:
    result = []
    choices = {i for i in range(persons)}
    for msg in message_list:
        actual = random.sample(choices, k=ring_order)
        if msg not in actual:
            actual[0] = msg
        result.append(actual)
    return result


def get_choices(weights: List[int], k: int):
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
    result = []
    weights = [1] * persons
    for msg in message_list:
        w = list(weights)
        w[msg] = 0
        actual = get_choices(w, ring_order-1)
        actual.append(msg)
        result.append(actual)
        for i in actual:
            weights[i] += 1
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


