import random
import typing

from src.context import Context

def simulate(
        context: Context,
        # message_function: typing.Callable[[Context], list[int]],
        group_encrypter: typing.Callable[[Context, list[int]], list[list[int]]],
        seed: int | None = None,
):
    # msg_list = message_function(context)
    # random.seed(seed)
    msg_list = random.sample(context.message_list, len(context.message_list))
    return group_encrypter(context, msg_list)
