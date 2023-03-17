import random
import typing
import dataclasses as dto

from src.context import Context


@dto.dataclass
class Simulation:
    context: Context
    seed: int | None
    msg_list: list[int]
    signature: list[list[int]]


def simulate(
    context: Context,
    # message_function: typing.Callable[[Context], list[int]],
    group_encrypter: typing.Callable[[Context, list[int]], list[list[int]]],
    seed: int | None = None,
):
    # msg_list = message_function(context)
    # random.seed(seed)
    msg_list = random.sample(context.message_list, len(context.message_list))
    return Simulation(
        context=context,
        seed=seed,
        msg_list=msg_list,
        signature=group_encrypter(context, msg_list),
    )
