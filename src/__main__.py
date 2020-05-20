import random
import sys
import src.simulator as sim
import src.zipf as zf
from functools import reduce


def probability(num_people, k, messages, num_loop):
    for i in range(num_loop):
        rnd_msgs = random.sample(messages, k=len(messages))
        sims = sim.simulation(num_people, k, rnd_msgs)
        yield sim.probability_of_all(num_people, rnd_msgs, sims)


def main():
    if len(sys.argv) != 4:
        print("Usage: python -m src <num_people> <k> <max_msg> <num-loop>")
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:]))
    messages = zf.zipf(num_people, max_msg, 1.5)
    probs = list(map(lambda x: x / num_loop,
        reduce(lambda ls1, ls2: [a + b for a, b in zip(ls1, ls2)], probability(num_people, k, messages, num_loop))))
    print(probs)

if __name__ == '__main__':
    main()
