import functools
import dataclasses as dto
import typing

from src.simulation import Simulation


@dto.dataclass
class User:
    pk: int
    messages: int
    signatures: int

    @property
    def anonymity(self):
        if self.messages == 0:
            return self.signatures  # a user that do not exist
        return self.signatures / self.messages

    def to_csv_row(self):
        return f"{self.pk}, {self.messages}, {self.signatures}"


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


def anonymity_score(simulation: Simulation) -> list[User]:
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
    return [User(i, msgcount[i], sim[i]) for i in range(simulation.context.people)]


def anonymity_window(window: int) -> typing.Callable[[Simulation], list[User]]:
    """
    Computes probability s.t. how many messages has firstly send in the window in the signature vs.
    how many real messages has been sent that way.
    """

    def a(simulation: Simulation) -> list[User]:
        assert_msg = f"Window should be bigger than msg_list: {window} >= {len(simulation.msg_list)}"
        assert window < len(simulation.msg_list), assert_msg
        broken = [0 for _ in range(simulation.context.people)]
        total = [0 for _ in range(simulation.context.people)]
        window_list = [0 for _ in range(simulation.context.people)]
        for signature in simulation.signature[:window]:
            for user in signature:
                total[user] += 1
        n = 0
        for i, signature in enumerate(simulation.signature[window:], start=window):
            for user in signature:
                if window_list[user] == 0:
                    n += 1
                    total[user] += 1
                    if simulation.msg_list[i] == user:
                        broken[user] += 1
                window_list[user] += 1
            for user in simulation.signature[i - window]:
                window_list[user] -= 1
        return [User(i, broken[i], total[i]) for i in range(simulation.context.people)]

    return a
