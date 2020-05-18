from src.simulator import *
import matplotlib.pyplot as plt
import numpy as np


def main():
    persons = 7
    messages = [1, 4, 6, 2, 6, 3, 1]
    sim = simulation_weighted(persons, 3, messages)
    probs = probability_of_all(persons, messages, sim)
    plt.hist(probs)
