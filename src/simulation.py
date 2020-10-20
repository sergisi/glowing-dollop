from src.data import Context
from src.distribution import Zipf


class Simulation:

    def __init__(self, context: Context):
        self.context = context
        self.msg_list = None

    def simulate(self, seed=None):
        import random
        self.msg_list = self.context.distribution().messages()
        random.seed(seed)
        self.msg_list = random.sample(self.msg_list, len(self.msg_list))
        choice = self.context.choice(self.msg_list)
        return choice.apply()


def main():
    persons, ring_order, max_msg = 200, 4, 15
    simulation: Simulation = Simulation(
        persons, ring_order, PAttachBuilder().set_weight(1))
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    first_signatures = simulation.simulate(zipf)[:10]
    print(first_signatures)


if __name__ == "__main__":
    main()
