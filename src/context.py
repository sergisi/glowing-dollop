import typing
import functools
import dataclasses as dto


@dto.dataclass
class Context:
    """
    Context of the simulation. It just stores some data that is needed to generate the messages,
    probabilities, choices and everything.

    Note that ring_order < people, but it is not checked programatically.
    """

    people: int
    ring_order: int
    distribution: typing.Callable[["Context"], list[int]]

    @functools.cached_property
    def message_list(self):
        return self.distribution(self)

    def __repr__(self):
        return f"Context({self.people=}, {self.ring_order=}, {self.message_list=})"
