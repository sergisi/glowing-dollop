from typing import List, Dict
from collections import defaultdict
import random

# corroutine(msg)
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
        choices.append(actual)
    return result

def simulation_to_dictionary(simulation: List[List[int]]) -> Dict[int, List[int]]:
    dic = defaultdict(list)
    for i, ls in enumerate(simulation):
        for person in ls:
            dic[person].append(i)
    return dic

