import sys
import argparse
from multiprocessing.context import Process

from src.analysis import *
from src.data import PreferentialContext, UniformContext, Context
from src.simulation import Simulation


def parse():
    parser = argparse.ArgumentParser(description="Simulation of anonymum forum")
    parser.add_argument('k', metavar='K', type=int, help='The order of ring signature')
    parser.add_argument('--people', '-p', metavar='people', type=int, help='Quantity of people in the distribution',
                        default=200)
    parser.add_argument('-s', metavar='s', type=float, help='s constant of Zipf Distribution', default=1.4)
    parser.add_argument('--max', metavar='max_msgs', type=int, help='Maximum amount of messages from one only author',
                        default=15)
    parser.add_argument('--seed', metavar='seed', type=int, help='Number of seeds', default=50)
    parser.add_argument('--sweight', metavar='weight', type=int, help='Value of weight for each signature', default=1)
    parser.add_argument('--fweight', metavar='weight', type=int, help='Value of weight for each signature', default=1)
    parser.add_argument('--siweight', metavar='weight', type=int, help='Value of weight for each signature', default=1)
    parser.add_argument('--fiweight', metavar='weight', type=int, help='Value of weight for each signature', default=200)
    parser.add_argument('--output', '-o', metavar='output', type=str, help='output dir', default='./output/best/')
    return parser.parse_args()


def main():
    args = parse()
    PEOPLE = args.people
    K = args.k
    SEED_RANGE = args.seed
    SW, FW = args.sweight, args.fweight
    SIW, FIW = args.siweight, args.fiweight
    output = args.output + f'{SEED_RANGE}-{K}'
    context: PreferentialContext = PreferentialContext(people=PEOPLE, k=K, max_msg=args.max, s=args.s, initial_weight=1,
                                           weight=1)
    NUM_THREADS = 4
    for w in range(SW, FW + 1):
        for iw in range(SIW, FIW+1):
            print(iw, w)
            filename: str = f'{output}/iw{iw}-w{w}.csv'
            writer = open(filename, mode='w+')
            print('seed', 'initial-weight', 'weight', 'none-anonymity',
                  'mean', 'median', 'desviation', 'min', 'max', 'range',
                  'person1', 'person5', 'person10', 'person15',
                  sep=',', file=writer)
            writer.close()
            context = context.new_weight(w).new_initial_weight(iw)
            process = {}
            for m in range(NUM_THREADS):
                start = int(SEED_RANGE/NUM_THREADS * m)
                finish = int(SEED_RANGE/NUM_THREADS * (m + 1))
                process[m] = Process(target=thread_calculation, args=(start, finish, iw, context, w, filename,))
                process[m].start()
            for m in range(NUM_THREADS):
                process[m].join()


def thread_calculation(start, finish, iw, context, w, filename):
    for s in range(start, finish + 1):
        sim: Simulation = Simulation(context)
        signs = sim.simulate(s)
        scorer: AnonymityScorer = context.scorer()
        msgs = context.messages()
        reviewer = ReviewerChanger(signs, scorer, msgs)
        finder: PeopleFinder = PeopleFinder(signs, scorer, context)
        mean = reviewer.apply(lambda x: sum(x) / len(reviewer.scores))
        median = MedianReviewer(signs, scorer).review(msgs)
        n_an = AnonymityReviewer(signs, scorer).review(msgs)
        minimum = reviewer.apply(min)
        maximum = reviewer.apply(max)
        desviation = MediumDesviation(signs, scorer, mean).review(msgs)
        rang = (maximum - minimum)
        p1, p5, p10, p15 = list(map(lambda x: finder.apply(x), [1, 5, 10, 15]))
        writer = open(filename, mode='a+')
        print(s, iw, w, n_an, mean, median, desviation, minimum, maximum, rang, p1, p5, p10, p15, sep=',',
              file=writer)
        writer.close()


if __name__ == '__main__':
    main()
