import typing
from src.context import Context

Choice = typing.Callable[[Context], list[list[int]]]
