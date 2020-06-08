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
        print(f'{k} & ', file=out_file, end='')
        values = get_probs(200, k, 15, 10, s, simulation)
        print(' & '.join(str(list(map(lambda x: round(x, 4), values)))[1:-1].split(', ')) + r'\\', file=out_file)
        yield values
    print(r'\hline', file=out_file)


def show_average(k_range, s_range, simulation, prefix):
    for s in s_range:
        with open(f'{prefix}{int(s*10)}.tex', 'w') as out_file:
            print(r'\begin{table}[H]', file=out_file)
            print(r'\centering', file=out_file)
            print(r'\begin{tabular}{c|ccc}', file=out_file)
            print(r'K &1msm &5msm &15msm\\', file=out_file)
            print(r'\hline', file=out_file)
            values = map(lambda x: x / len(k_range), reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]),
                                                 gen(k_range, s, simulation, out_file)))
            print('& ' + ' & '.join(str(list(map(lambda x: round(x, 4), values)))[1:-1].split(', ')) + r'\\', file=out_file)
            print(r'\end{tabular}', file=out_file)
            print(r'\caption{S:' + f'{s}' + r'}', file=out_file)
            print(r'\label{tab:s'f'{s}'r'}', file=out_file)
            print(r'\end{table}', file=out_file)


def main():
    if len(sys.argv) == 1:
        s_range = list(map(lambda x: x / 10, range(13, 21)))
        k_range = list(range(3, 13))
        show_average(k_range, s_range, sim.preferential_attachment_simulation, 'doc/tab/prefatach/')
        show_average(k_range, s_range, sim.uniform_simulation, 'doc/tab/uniform/')
        sys.exit()
    if len(sys.argv) != 6:
        print('Usage: python -m src <num_people> <k> <max_msg> <num-loop> <s-zipf> ')
        print('Usage: python -m src')
        sys.exit()
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:-1]))
    s = float(sys.argv[-1])
    get_probs(num_people, k, max_msg, num_loop, s, sys.stdout)


if __name__ == '__main__':
    main()
