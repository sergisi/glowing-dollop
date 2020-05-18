from src.simulator import *
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    persons = 7
    messages = [1, 4, 6, 2, 6, 9, 1]
    sim = simulation_weighted(persons, 7, messages)
    probs = probability_of_all(persons, messages, sim)
    plt.hist(probs)
