from typing import List

from src.analysis.scorer import UnlinkabilityScorer as Scorer
from src.data import PreferentialContext
from src.simulation import Simulation
from src.distribution import Zipf


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


def test(context: PreferentialContext):
    sim = Simulation(context)
    signature = sim.simulate()
    reviewer = Reviewer(signature, Scorer(context.get_people()))
    print(context.get_weight(), reviewer.review(sim.msg_list))

def main():
    Context = PreferentialContext(200, 6, 15, 1.3, 1,1)
    for w in range(1,2,3):
        test(Context.new_weight(w))



if __name__ == "__main__":
    main()
