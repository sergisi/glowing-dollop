import functools
from typing import List

from src.data import PreferentialContext
from src.simulation import Simulation

def __simulation_to_dictionary(simulation: Simulation) -> list[int]:
    """
    Parses a result of a simulations to a
    List of integers, where the nth position is the
    number of messages that this person has signed.
    :param people -> int : number of people in the simulation
    :param signatures -> List[List[int]] : result of a simulation
    :return List[int] : the nth position is the number
        of messages that the nth persone has signed
    """
    res = [0] * simulation.context.people
    for ls in simulation.signature:
        for person in ls:
            res[person] += 1
    return res

def __get_messagecount(simulation: Simulation) -> list[int]:
    """
    Parses a message_list and counts the number of messages send by a
    """
    msgcount = [0] * simulation.context.people
    for i in simulation.msg_list:
        msgcount[i] += 1
    return msgcount

def anonymity_score(simulation: Simulation) -> list[int]:
    """
    Parses a the simulation result (signatures) into a list containing
    in the nth value the anounimosity of the nth person. The common
    practice should be:
        def a(persons, k, message_list):
            sim = simulation(persons, k, message_list)
            return probability_of_all(persons, message_list, sim)
    But this way is more flexible (you can study the way that the numbers
    are choosen as you already have the simulation, for example)

    Changed the parameters. As the new design is centered around DTOs and methods,
    this avoid the shotgun code smell that was appearing in all the code.

    :param persons -> int : number of persons in the simulation.
    """
    sim = __simulation_to_dictionary(simulation)
    msgcount = __get_messagecount(simulation)
    return [
        sim[i] / msgcount[i] if msgcount[i] != 0 else 0 for i in range(simulation.context.people)
    ]


