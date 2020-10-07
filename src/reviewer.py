from scorer import PrivacityScorer
from typing import List
from simulation import Simulation
from distribution import Zipf

class Reviewer:

    def __init__(self, signature: List[List[int]], scorer: PrivacityScorer):
        self.signature = signature
        self.scorer: PrivacityScorer = scorer

    def review(self, list_msgs: List[int]):
        scores = list(PrivacityScorer(persons).get_scores(simulation.list_msgs, signature))
        print(scores)

if __name__ == "__main__":
    persons, ring_order, max_msg = 200, 4, 15
    simulation: Simulation = Simulation(persons, ring_order, 1)
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    signature = simulation.simulate(zipf)
    reviewer = Reviewer(signature, PrivacityScorer(persons))
    reviewer.review(simulation.list_msgs)
