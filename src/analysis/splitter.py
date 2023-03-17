"""
Users should be grouped, as different number of signatures
have different exploits.

What we are looking for is if a group after a quantile is exploitable.
For example, if the lurkers that remeain lurkers don't have any privacy
as a mean, or if the superusers don't have as much privacy as a mean.


Idea
---------

Split:
  lurker: list[User]
  normal: list[User]
  superuser: list[User]

Simulation -> quantile1 -> quantile2 -> Split

Methods to describe all of them.

"""
import dataclasses as dto
import functools

from .reviewer import *


@dto.dataclass
class SplitReview:
    simulation: Simulation
    users: list[User]
    first_quantile: float = 0.05
    second_quantile: float = 0.75

    @functools.cached_property
    def signatures(self) -> list[User]:
        return sorted(self.users, key=lambda x: x.signatures)

    @functools.cached_property
    def lurkers(self) -> list[User]:
        return list(self.signatures[: int(len(self.users) * self.first_quantile)])

    @functools.cached_property
    def normal_users(self) -> list[User]:
        start = int(len(self.users) * self.first_quantile)
        end = int(len(self.users) * self.second_quantile)
        return list(self.signatures[start:end])

    @functools.cached_property
    def superusers(self) -> list[User]:
        start = int(len(self.users) * self.second_quantile)
        return list(self.signatures[start:])

    def describe(self):
        """
        Describes the three groups:
        """
        return " |\n".join(
            [
                "| lurkers    | " + Review(self.simulation, self.lurkers).describe(),
                "| users      | "
                + Review(self.simulation, self.normal_users).describe(),
                "| superusers | "
                + Review(self.simulation, self.superusers).describe()
                + " |",
            ]
        )
