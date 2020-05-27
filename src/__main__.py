import random
import sys
import src.simulator as sim
import src.zipf as zf
from functools import reduce
from collections import Counter


def probability(num_people, k, messages, num_loop, simulation):
    for i in range(num_loop):
        random.seed(i)
        rnd_msgs = random.sample(messages, k=len(messages))
        sims = simulation(num_people, k, rnd_msgs)
        yield sim.probability_of_all(num_people, rnd_msgs, sims)


def get_probs(num_people, k, max_msg, num_loop, s, simulation):
    def person_of(num_msgs):
        return lambda x: x[1] == num_msgs

    def get(num, msgs):
        return list(filter(person_of(num), Counter(msgs).most_common()))[0]

    messages = zf.zipf(num_people, max_msg, s)
    p15, p5, p1 = [get(num, messages)[0] for num in [15, 5, 1]]
    probs = list(map(lambda x: x / num_loop,
                     reduce(lambda ls1, ls2: [a + b for a, b in zip(ls1, ls2)],
                            probability(num_people, k, messages, num_loop, simulation))))
    return probs[p1], probs[p5], probs[p15]


def gen(k_range, s, simulation, out_file):
    for k in k_range:
        print("k:", k, file=out_file)
        values = get_probs(200, k, 15, 10, s, simulation)
        print(values, file=out_file)
        yield values


def show_average(k_range, s_range, simulation, out_file):
    for s in s_range:
        print("\t======== S:", s, "========", file=out_file)
        m15, m10, m1 = map(lambda x: x / 10, reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]),
                                                    gen(k_range, s, simulation, out_file)))
        print("M:", m15, m10, m1, file=out_file)


def main():
    if len(sys.argv) == 1:
        s_range = list(map(lambda x: x / 10, range(13, 21)))
        k_range = [4, 6, 8, 10, 12]
        with open("out/prefential.txt", mode="w") as file:
            show_average(k_range, s_range, sim.preferential_attachment_simulation, file)
        with open("out/uniform.txt", mode="w") as file:
            show_average(k_range, s_range, sim.uniform_simulation, file)
        sys.exit()
    if len(sys.argv) != 6:
        print("Usage: python -m src <num_people> <k> <max_msg> <num-loop> <s-zipf> ")
        print("Usage: python -m src")
        sys.exit()
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:-1]))
    s = float(sys.argv[-1])
    get_probs(num_people, k, max_msg, num_loop, s, sys.stdout)


if __name__ == '__main__':
    main()
