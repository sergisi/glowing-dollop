from src.analysis.scorer import UnlinkabilityScorer as Scorer
from src.simulation import Simulation
from src.distribution import Zipf
from src.choices.patterns import *


class Reviewer:

    def __init__(self, signature: List[List[int]], scorer: Scorer):
        self.signature = signature
        self.scorer: Scorer = scorer

    def review(self, list_msgs: List[int]):
        scores = list(
            enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        if any(map(lambda x: x[1] <= 1.0, scores)):
            people_visible = list(filter(lambda x: x[1] == 1.0, scores))
            signs = map(lambda p: list(
                filter(lambda x: p[0] in x, self.signature)), people_visible)
            return "BAD WEIGHT", people_visible, list(signs)
        else:
            return "OK"


def test(choice_builder, people, ring_order, max_msg, w, s=1.3):
    choice_builder = choice_builder.reset()
    if isinstance(choice_builder, WeightBuilder):
        choice_builder.set_weight(w)
    simulation: Simulation = Simulation(people, ring_order, choice_builder)
    zipf: Zipf = Zipf(people, max_msg, s)
    signature = simulation.simulate(zipf)
    reviewer = Reviewer(signature, Scorer(people))
    print(w, reviewer.review(simulation.list_msgs))


def test_loop(choice_builder):
    people, ring_order, max_msg = 200, 12, 15
    for w in [e for e in range(3)]:
        test(choice_builder, people, ring_order, max_msg, w)


def main():
    """
    test_loop(UniformBuilder())
    test_loop(PAttachBuilder().set_weight(1))
    test_loop(UniquePAttachBuilder().set_weight(1))
    test_loop(UniquePAttachBuilder().set_weight(2))
    """
    test_loop(ThresholdBuilder().set_weight(1))
    test_loop(ThresholdBuilder().set_weight(2))



if __name__ == "__main__":
    main()
