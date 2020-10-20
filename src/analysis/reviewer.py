from abc import ABC, abstractmethod
from typing import List

from src.analysis.scorer import AnonymityScorer as Scorer
from src.data import PreferentialContext
from src.simulation import Simulation
from src.distribution import Zipf


class Reviewer(ABC):

    def __init__(self, signature: List[List[int]], scorer: Scorer):
        self.signature = signature
        self.scorer: Scorer = scorer

    @abstractmethod
    def review(self, list_msgs: List[int]):
        pass


class AnonymityReviewer(Reviewer):

    def __init__(self, signature: List[List[int]], scorer: Scorer):
        super().__init__(signature, scorer)

    def review(self, list_msgs: List[int]):
        scores = list(
            enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        people_visible = list(filter(lambda x: x[1] == 1.0, scores))
        return len(people_visible)


class OutlierMeanReviewer(Reviewer):

    def review(self, list_msgs: List[int]):
        scores = list(enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        mean = sum(map(lambda x: x[1], scores)) / len(scores)
        max_an = max(map(lambda x: x[1], scores))
        min_an = min(map(lambda x: x[1], scores))
        return mean - min_an, max_an - mean


class OutlierMedianReviewer(Reviewer):

    def review(self, list_msgs: List[int]):
        scores = list(enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        sorted_list = sorted(scores, key=lambda x: x[1])
        median = sorted_list[int(len(scores)/2)]
        max_an = max(map(lambda x: x[1], scores))
        min_an = min(map(lambda x: x[1], scores))
        return median - min_an, max_an - median


def test(context: PreferentialContext):
    sim = Simulation(context)
    signature = sim.simulate()
    reviewer = AnonymityReviewer(signature, Scorer(context.get_people()))
    print(context.get_weight(), reviewer.review(sim.msg_list))


def main():
    Context = PreferentialContext(200, 6, 15, 1.3, 1, 1)
    for w in range(1, 2, 3):
        test(Context.new_weight(w))


if __name__ == "__main__":
    main()
