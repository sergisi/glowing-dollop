import random
import sys
import src.simulator as sim
import src.zipf as zf


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python -m src <num_people> <k> <max_msg> <num-loop>")
    num_people, k, max_msg, num_loop = list(map(int, sys.argv[1:]))
    messages = zf.zipf(num_people, max_msg)
    for i in range(num_loop):
        rnd_msgs = random.sample(messages, k=len(messages))
        sims = sim.simulation(num_people, k, rnd_msgs)
        print(sim.probability_of_all(num_people, rnd_msgs, sims))




