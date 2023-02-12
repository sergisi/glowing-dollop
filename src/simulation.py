import random
import typing

from src.context import Context

def simulate(
        context: Context,
        # message_function: typing.Function[[Context], list[int]],
        group_encrypter_simulator: typing.Function[[Context, list[int]], list[list[int]]],
        seed: int | None = None,
):
    # msg_list = message_function(context)
    # random.seed(seed)
    msg_list = random.sample(context.message_list, len(context.message_list))
    return group_encrypter(msg_list)
