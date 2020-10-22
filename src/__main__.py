import sys
from src.analysis import *
from src.data import PreferentialContext
from src.simulation import Simulation


def main():
    context: PreferentialContext = PreferentialContext(people=200, k=6, max_msg=15, s=1.4, initial_weight=1, weight=1)

    for w in range(1, 4 + 1):
        for iw in range(1, 201):
            print(w, '-',iw)
            writer = open(f'./output/file-{iw}-{w}.csv', mode='w+')
            print('initial_weight', 'weight', 'none-anonymity', 'mean-min', 'max-mean', 'median-min', 'max-median',
                  sep=',', file=writer)
            context = context.new_weight(w).new_initial_weight(iw)
            for s in range(1, 200):
                sim: Simulation = Simulation(context)
                signs = sim.simulate(s)
                scorer: AnonymityScorer = context.scorer()
                om0, om1 = OutlierMeanReviewer(signs, scorer).review(context.messages())
                od0, od1 = OutlierMedianReviewer(signs, scorer).review(context.messages())
                print(iw, w, AnonymityReviewer(signs, scorer).review(context.messages()), om0, om1, od0, od1, sep=',',
                      file=writer)
            writer.close()


if __name__ == '__main__':
    main()
