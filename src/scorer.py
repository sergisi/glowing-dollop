from typing import List
from distribution import Zipf
from simulation import Simulation
from choice import PAttachBuilder
from functools import reduce
from collections import Counter

class PrivacityScorer:

    def __init__(self, persons: int):
        self.persons = persons

    def __simulation_to_dictionary(self, signatures: List[List[int]]) -> List[int]:
        """
        Parses a result of a simulations to a 
        List of integers, where the nth position is the 
        number of messages that this person has signed.
        :param persons -> int : number of persons in the simulation
        :param signatures -> List[List[int]] : result of a simulation
        :return List[int] : the nth position is the number 
            of messages that the nth persone has signed
        """
        res = [0] * self.persons
        for ls in signatures:
            for person in ls:
                res[person] += 1
        return res


    def __get_messagecount(self, message_list: List[int]) -> List[int]:
        """
            Parses a message_list and counts the number of messages send by a     
        """
        msgcount = [0] * self.persons
        for i in message_list:
            msgcount[i] += 1
        return msgcount


    def get_scores(self, message_list: List[int], signatures: List[List[int]]):
        """
            Parses a the simulation result (signatures) into a List containing 
            in the nth value the anounimosity of the nth person. The common 
            practice should be:
                def a(persons, k, message_list):
                    sim = simulation(persons, k, message_list)
                    return probability_of_all(persons, message_list, sim)
            But this way is more flexible (you can study the way that the numbers 
            are choosen as you already have the simulation, for example)
            :param persons -> int : number of persons in the simulation.
            :param message_list -> List[int]: 
                list of messages used in the simulation.
            :param signatures -> List[List[int]]: result of the simulation.
            :return List[int]: 
                Returns a list of floating numbers where the nth position has that 
                level of anounimosity.
        """
        sim = self.__simulation_to_dictionary(signatures)
        msgcount = self.__get_messagecount(message_list)
        return [sim[i] / msgcount[i] if msgcount[i] != 0 else 0
                for i in range(self.persons)]


def main():
    persons, ring_order, max_msg = 200, 4, 15
    simulation: Simulation = Simulation(persons, ring_order, 200)
    zipf: Zipf = Zipf(persons, max_msg, 1.3)
    signature = simulation.simulate(zipf)
    print(signature[:10])
    scores = PrivacityScorer(persons).get_scores(simulation.list_msgs, signature)
    get_scores = lambda xs: [(elem, scores[elem]) for elem in reduce(lambda x, y: x.union(y),map(lambda x: set(x), xs))]
    print(get_scores(signature))
    maximum = max(get_scores(signature), key = lambda x: x[1])
    minimum = min(get_scores(signature), key = lambda x: x[1])
    print(maximum, minimum)

if __name__ == "__main__":
    main()