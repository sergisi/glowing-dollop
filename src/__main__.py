import random
import sys
import src.simulator as sim
import src.zipf as zf
from functools import reduce
from collections import Counter


def probability(num_people, k, messages, num_loop):
    for i in range(num_loop):
        random.seed(i)
        rnd_msgs = random.sample(messages, k=len(messages))
        sims = sim.simulation(num_people, k, rnd_msgs)
        yield sim.probability_of_all(num_people, rnd_msgs, sims)


def main(num_people, k, max_msg, num_loop, s):
    def person_of(num_msgs):
        return lambda x: x[1] == num_msgs

    def get(num, msgs):
        return list(filter(person_of(num), Counter(msgs).most_common()))[0]

    messages = zf.zipf(num_people, max_msg, s)
    p15, p5, p1 = [get(num, messages)[0] for num in [15, 5, 1]]
    probs = list(map(lambda x: x / num_loop,
                     reduce(lambda ls1, ls2: [a + b for a, b in zip(ls1, ls2)],
                            probability(num_people, k, messages, num_loop))))
    return probs[p1], probs[p5], probs[p15]


def gen(k_range, s):
    for k in k_range:
        print("k:", k)
        values = main(200, k, 15, 10, s)
        print(values)
        yield values


if __name__ == '__main__':
    if len(sys.argv) == 1:
        s_range = list(map(lambda x: x / 10, range(13, 21)))
        k_range = [4, 6, 8, 10, 12]
        for s in s_range:
            print("\t======== S:", s, "========")
            m15, m10, m1 = map(lambda x: x / 10, reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]),
                                                        gen(k_range, s)))
            print("M:", m15, m10, m1)
        sys.exit()
    if len(sys.argv) != 6:
        print("Usage: python -m src <num_people> <k> <max_msg> <num-loop> <s-zipf> ")
        print("Usage: python -m src")
        sys.exit()
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:-1]))
    s = float(sys.argv[-1])
    main(num_people, k, max_msg, num_loop, s)
