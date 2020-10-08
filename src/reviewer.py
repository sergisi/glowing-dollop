from scorer import PrivacityScorer
from typing import List
from simulation import Simulation
from distribution import Zipf
from choices.patterns import PAttachBuilder

class Reviewer:

    def __init__(self, signature: List[List[int]], scorer: PrivacityScorer):
        self.signature = signature
        self.scorer: PrivacityScorer = scorer

    def review(self, list_msgs: List[int]):
        scores = list(enumerate(self.scorer.get_scores(list_msgs, self.signature)))
        if any(map(lambda x: x[1] <= 1.0 ,scores)):
            people_visible = list(filter(lambda x: x[1] == 1.0, scores))
            signs = map(lambda p: list(filter(lambda x: p[0] in x, self.signature)), people_visible)
            return "BAD WEIGHT", people_visible, list(signs)
        else:
            return "OK"

def main():
    persons, ring_order, max_msg = 200, 12, 15
    for w in [e  for e in range(3)]:
        simulation: Simulation = Simulation(persons, ring_order, w, PAttachBuilder())
        zipf: Zipf = Zipf(persons, max_msg, 1.3)
        signature = simulation.simulate(zipf)
        reviewer = Reviewer(signature, PrivacityScorer(persons))
        print(w, reviewer.review(simulation.list_msgs))

if __name__ == "__main__":
    main()
