"""
    Module for generating zipf instances. The way of doing it is
    to generate a zipfg. Then sample it with:
        random.sample(ls, k=len(ls))
"""

from typing import Generator, TypeVar, List


def correct_msm(number_persons, persons):
    total_people = sum(int(x) for x in number_persons)
    if total_people == persons:
        return [int(x) for x in number_persons]
    res = list(sorted(enumerate(number_persons), key=lambda x: x[1] - int(x[1])))
    for n in range(1, persons - total_people + 1):
        res[-n] = (res[-n][0], res[-n][1] + 1)
    res = sorted(res)
    return [int(x[1]) for x in res]


def zipf(persons: int,
         maximum_messages: int, s: float = 2.5) -> List[int]:
    prob_msm = lambda x: 1 / (x ** s)
    total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
    number_persons = [prob_msm(x) * persons / total
                      for x in range(1, maximum_messages + 1)]
    # import pdb; pdb.set_trace()
    number_persons = correct_msm(number_persons, persons)
    messages: List[int] = []
    current_person = 0  # current person to add in the message list
    for it, i in enumerate(number_persons, 1):
        for _ in range(i):
            for _ in range(it):
                # adds number of messages of the current person
                messages.append(current_person)
            current_person += 1
    return messages
