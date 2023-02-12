"""
    Module for generating zipf instances. The way of doing it is
    to generate a zipfg. Then sample it with:
        random.sample(ls, k=len(ls))
"""
from src.context import Context
import typing


def uniform_distribution(context: Context) -> list[int]:
    return list(range(context.people))

def zipf_distribution(max_msg: int, s: float) -> typing.Callable[[Context], list[int]]:
    def a(context: Context) -> list[int]:
        return _zipf(context.people, max_msg, s)
    return a

def _correct_msm(number_persons, persons):
    total_people = sum(int(x) for x in number_persons)
    if total_people == persons:
        return [int(x) for x in number_persons]
    res = list(sorted(enumerate(number_persons), key=lambda x: x[1] - int(x[1])))
    for n in range(1, persons - total_people + 1):
        res[-n] = (res[-n][0], res[-n][1] + 1)
    res = sorted(res)
    return [int(x[1]) for x in res]

def _zipf(persons: int, maximum_messages: int, s: float = 2.5) -> list[int]:
    prob_msm = lambda x: 1 / (x**s)
    total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
    number_persons = [
        prob_msm(x) * persons / total for x in range(1, maximum_messages + 1)
    ]
    # import pdb; pdb.set_trace()
    number_persons = _correct_msm(number_persons, persons)
    messages: list[int] = []
    current_person = 0  # current person to add in the message list
    for it, i in enumerate(number_persons, 1):
        for _ in range(i):
            for _ in range(it):
                # adds number of messages of the current person
                messages.append(current_person)
            current_person += 1
    return messages


def main():
    zipf = _zipf(400, 15, 1.3)
    print(zipf)


if __name__ == "__main__":
    main()
