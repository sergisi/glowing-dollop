from choice import Choice, PreferentialAttachmentSim
from distribution import Distribution, Zipf
import random

class Simulation:

    def __init__(self, choice: Choice):
        self.__choice: Choice = choice

    def simulate(self, distribution: Distribution):
        list_msgs = distribution.messages()
        list_msgs = random.sample(list_msgs, len(list_msgs))
        return list_msgs

if __name__ == "__main__":
    persons, ring_order, max_msg = 200, 4, 15
    choice: Choice = PreferentialAttachmentSim(persons, ring_order, max_msg)
    simulation: Simulation = Simulation(choice)
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    first_people = simulation.simulate(zipf)[:10]
    print(first_people)
