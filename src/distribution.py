"""
    Module for generating zipf instances. The way of doing it is
    to generate a zipfg. Then sample it with:
        random.sample(ls, k=len(ls))
"""
from abc import ABC, abstractmethod
from typing import Generator, TypeVar, List


class Distribution(ABC):

    def __init__(self, persons: int):
        self.persons = persons

    @abstractmethod
    def messages(self):
        pass


class Zipf(Distribution):

    def __init__(self, persons: int, max_msg: int, s: float):
        super().__init__(persons)
        self.max_msg = max_msg
        self.s = s
        self.msgs = None

    @staticmethod
    def correct_msm(number_persons, persons):
        total_people = sum(int(x) for x in number_persons)
        if total_people == persons:
            return [int(x) for x in number_persons]
        res = list(sorted(enumerate(number_persons),
                          key=lambda x: x[1] - int(x[1])))
        for n in range(1, persons - total_people + 1):
            res[-n] = (res[-n][0], res[-n][1] + 1)
        res = sorted(res)
        return [int(x[1]) for x in res]

    def messages(self):
        if self.msgs is None:
            def prob_msm(x): return 1 / (x ** self.s)
            total = sum(prob_msm(y) for y in range(1, self.max_msg + 1))
            number_persons = [prob_msm(x) * self.persons / total
                            for x in range(1, self.max_msg + 1)]
            # import pdb; pdb.set_trace()
            number_persons = self.correct_msm(number_persons, self.persons)
            messages: List[int] = []
            current_person = 0  # current person to add in the message list
            for it, i in enumerate(number_persons, 1):
                for _ in range(i):
                    for _ in range(it):
                        # adds number of messages of the current person
                        messages.append(current_person)
                    current_person += 1
            self.msgs = messages
        return self.msgs


def zipf(persons: int,
         maximum_messages: int, s: float = 2.5) -> List[int]:
    prob_msm = lambda x: 1 / (x ** s)
    total = sum(prob_msm(y) for y in range(1, maximum_messages + 1))
    number_persons = [prob_msm(x) * persons / total
                      for x in range(1, maximum_messages + 1)]
    # import pdb; pdb.set_trace()
    number_persons = Zipf.correct_msm(number_persons, persons)
    messages: List[int] = []
    current_person = 0  # current person to add in the message list
    for it, i in enumerate(number_persons, 1):
        for _ in range(i):
            for _ in range(it):
                # adds number of messages of the current person
                messages.append(current_person)
            current_person += 1
    return messages


if __name__ == "__main__":
    zipf = Zipf(200, 15, 1.3)
    print(zipf.messages())