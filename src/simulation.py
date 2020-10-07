from choice import Choice, PreferentialAttachmentSim, ChoiceBuilder, PAttachBuilder
from distribution import Distribution, Zipf
import random

class Simulation:

    def __init__(self, persons: int, ring_order: int, weight: int):
        self.builder = PAttachBuilder().set_persons(persons).set_ring_order(ring_order).set_weight(weight)
        self.list_msgs = None

    def simulate(self, distribution: Distribution):
        self.list_msgs = distribution.messages()
        self.list_msgs = random.sample(self.list_msgs, len(self.list_msgs))
        self.builder.set_message_list(self.list_msgs)
        choice = self.builder.build()
        return choice.apply()

if __name__ == "__main__":
    persons, ring_order, max_msg = 200, 4, 15
    simulation: Simulation = Simulation(persons, ring_order, 100)
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    first_signatures = simulation.simulate(zipf)[:10]
    print(first_signatures)
    
