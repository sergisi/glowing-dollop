"""
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
        with open(f'{prefix}{int(s * 10)}.tex', 'w') as out_file:
            print(r'\begin{table}[H]', file=out_file)
            print(r'\centering', file=out_file)
            print(r'\begin{tabular}{c|ccc}', file=out_file)
            print(r'K &1msm &5msm &15msm\\', file=out_file)
            print(r'\hline', file=out_file)
            values = map(lambda x: x / len(k_range), reduce(lambda x, y: (x[0] + y[0], x[1] + y[1], x[2] + y[2]),
                                                            gen(k_range, s, simulation, out_file)))
            print('& ' + ' & '.join(str(list(map(lambda x: round(x, 4), values)))[1:-1].split(', ')) + r'\\',
                  file=out_file)
            print(r'\end{tabular}', file=out_file)
            simulation_name = simulation.__name__.replace("_", " ")
            print(r'\caption{Simulation method:'f'{simulation_name} S:{s}' + r'}', file=out_file)
            print(r'\label{tab:s'f'{s}'r'}', file=out_file)
            print(r'\end{table}', file=out_file)


def parse_arguments():
    parser = argparse.ArgumentParser(description='Simulation of an anonymous forum')

    parser.add_argument(f'-p', f'--num-people', dest=f'people',
                        type=int, default=200, help=f'Number of people')
    parser.add_argument(f'-kmin', f'--k-min-set', dest=f'kmin',
                        type=int, default=3, help=f'Minimum range of set')
    parser.add_argument(f'-kmax', f'--k-max-set', dest=f'kmax',
                        type=int, default=13, help=f'Maximum range of set')
    return parser.parse_args()


def main():
    parser = parse_arguments()
    s_range = list(map(lambda x: x / 10, range(13, 21)))
    k_range = list(range(parser.kmin, parser.kmax))
    show_average(k_range, s_range, sim.preferential_attachment_simulation, 'doc/tab/prefatach/')
    show_average(k_range, s_range, sim.uniform_simulation, 'doc/tab/uniform/')
    sys.exit()
"""


def simulation_main():
    from . import simulation as sim
    print("========== Simulation main ==========")
    sim.main()


def scorer_main():
    from . import scorer as sc
    print("========== Scorer main ==========")
    sc.main()


def reviewer_main():
    from . import reviewer as rv
    print("========== Reviewer main ==========")
    rv.main()


def distribution_main():
    from . import distribution as ds
    print("========== Distribution main ==========")
    ds.main()


def main():
    #simulation_main()
    scorer_main()
    #reviewer_main()
    #distribution_main()


if __name__ == '__main__':
    main()
