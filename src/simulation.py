from choice import Choice, PreferentialAttachmentSim, ChoiceBuilder
from distribution import Distribution, Zipf
import random

class Simulation:

    def __init__(self, builder: ChoiceBuilder):
        self.builder: ChoiceBuilder = builder
        self.list_msgs = None

    def simulate(self, distribution: Distribution):
        self.list_msgs = distribution.messages()
        self.list_msgs = random.sample(self.list_msgs, len(self.list_msgs))
        self.builder.set_message_list(self.list_msgs)
        
        return signatures

if __name__ == "__main__":
    persons, ring_order, max_msg = 200, 4, 15
    choice: Choice = PreferentialAttachmentSim(persons, ring_order, max_msg)
    simulation: Simulation = Simulation(choice)
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    first_people = simulation.simulate(zipf)[:10]
    print(first_people)
    
