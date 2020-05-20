import random
import sys
import src.simulator as sim
import src.zipf as zf
from functools import reduce
from collections import Counter


def probability(num_people, k, messages, num_loop):
    for i in range(num_loop):
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
    print(f"s: {s},\tk: {k},\tp1: {probs[p1]},\tp5: {probs[p5]},\tp15: {probs[p15]}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        for s in map(lambda x: x / 10, range(13, 21)):
            for k in [4, 6, 8, 10, 12]:
                main(200, k, 15, 10, s)
        sys.exit()
    if len(sys.argv) != 6:
        print("Usage: python -m src <num_people> <k> <max_msg> <num-loop> <s-zipf> ")
        print("Usage: python -m src")
        sys.exit()
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:-1]))
    s = float(sys.argv[-1])
    main(num_people, k, max_msg, num_loop, s)
