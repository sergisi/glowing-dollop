import typing
import dataclasses as dto
import functools

from .scorer import anonymity_score
from src.simulation import Simulation

@dto.dataclass
class Review:
    """
    # Review a Simulation.

    The purpose of this class is to provide a painless way to generate stats
    about a Simulation.

    The general methodology will be to first provide the Simulation, and optionally
    a scorer, although I don't know when it will be nice to have.

    Then, the implementation of this class is to have a bunch of cached properties,
    so if you need the mean, median, max, min of the anonymity of the class you can
    have it by a simple property, and meaningful but partially results can be used
    for all of the statistics.

    This simplifies the architecture of having a thousand classes to provide this blocks,
    albait due to python non extensible classes (and I mean Kotlin-like, not hierarchy based),
    it may grow into a large class, although all of the methods should have 2 lines of code.

    :params simulation: the simulation to perform statistics to.
    :params scorer: the score function. For each identification it provides a score, that is,
        the total messages that an id has signed divided by the real messages that has posted.
        If it's one, then there is somobody that all its messages that he appeared have been posted
        by them.

    """
    simulation: Simulation
    scorer: typing.Callable[[Simulation], list[float]] = anonymity_score

    @functools.cached_property
    def scores(self) -> list[tuple[int, float]]:
        return sorted(list(enumerate(self.scorer(self.simulation))), key=lambda x: x[1])

    @functools.cached_property
    def anonymity(self) -> int:
        """
        Returns how many people do not have any anonimity. It could be improved
        efficiently with a take-while instead of a filter, but I do not care.
        """
        people_visible = list(filter(lambda x: x[1] == 1.0, self.scores))
        return len(people_visible)

    @functools.cached_property
    def medium_desviation(self) -> float:
        scores = self.scores
        return sum(map(lambda x: abs(x[1] - self.mean), scores)) / len(scores)

    # Note: there was a HOF function and a PeopleFinder class that I do not know
    # what they were or why they were useful. No docs provided, no code used.

    @functools.cached_property
    def mean(self) -> float:
        scores = self.scores
        return sum(map(lambda x: x[1], scores)) / len(scores)

    @property
    def median(self) -> float:
        scores = self.scores
        return scores[int(len(scores) / 2)][1]

    @property
    def min(self) -> float:
        return self.scores[0][1]

    @property
    def max(self) -> float:
        return self.scores[-1][1]

    def describe(self, sep=' | '):
        return sep.join(str(x) for x in
                        [self.anonymity,
                         self.medium_desviation,
                         self.mean,
                         self.median,
                         self.min,
                         self.max,
                         len(self.simulation.msg_list),
                         len(self.simulation.msg_list) * self.simulation.context.ring_order,
                         ])
