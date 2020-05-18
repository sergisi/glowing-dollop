"""
    Module for generating zipf instances. The way of doing it is
    to generate a zipfg. Then sample it with:
        random.sample(ls, k=len(ls))
"""

from typing import Generator, TypeVar

T = TypeVar('T')

def zipf(persons: int,
        maximum_messages: int, s: float = 2.5) -> List[int]:
    pass


