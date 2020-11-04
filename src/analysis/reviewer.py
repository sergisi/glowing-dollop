from abc import ABC, abstractmethod
from typing import List

from .scorer import AnonymityScorer as Scorer
from src.data import PreferentialContext, Context
from src.simulation import Simulation


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


class MediumDesviation(Reviewer):

    def __init__(self, signature: List[List[int]], scorer: Scorer, mean: int):
        super().__init__(signature, scorer)
        self.mean = mean

    def review(self, list_msgs: List[int]):
        scores = list(
            enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        return sum(map(lambda x: abs(x[1] - self.mean), scores)) / len(scores)


class ReviewerChanger:

    def __init__(self, signature, scorer, list_msgs):
        self.signature = signature
        self.scorer: Scorer = scorer
        self.scores = list(
            enumerate(self.scorer.get_scores(list_msgs, self.signature)))

    def apply(self, fun_outer, fun_inner=lambda x: x[1]):
        return fun_outer(map(fun_inner, self.scores))


class PeopleFinder:

    def __init__(self, signature, scorer, context: Context):
        self.signature = signature
        self.scorer: Scorer = scorer
        self.scores = list(
            enumerate(self.scorer.get_scores(context.messages(), self.signature)))
        self.context = context

    def apply(self, num_msgs):
        from collections import Counter
        counter = Counter(self.context.messages())
        index = filter(lambda x: x[1] == num_msgs, counter.most_common()) \
            .__next__()[0]
        return filter(lambda x: x[0] == index, self.scores) \
            .__next__()[1]


class MeanReviewer(Reviewer):

    def review(self, list_msgs: List[int]):
        scores = list(enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        mean = sum(map(lambda x: x[1], scores)) / len(scores)
        return mean


class MedianReviewer(Reviewer):

    def review(self, list_msgs: List[int]):
        scores = list(enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        sorted_list = sorted(scores, key=lambda x: x[1])
        median = sorted_list[int(len(scores) / 2)][1]
        return median


def test(context: PreferentialContext):
    sim = Simulation(context)
    signature = sim.simulate()
    finder = PeopleFinder(signature, Scorer(context.get_people()), context)
    print(finder.apply(1), finder.apply(5), finder.apply(15))


def main():
    context = PreferentialContext(200, 6, 15, 1.3, 1, 1)
    test(context)


if __name__ == "__main__":
    main()
