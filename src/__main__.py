"""
Main module. Contains some scripts.

The design of the CLI is by typer. This will let us hack around more easily, which at the
end is what we want.


"""
from . import simulation, distribution, context
from .choices import preferential_attachment_choice, timely_attachment_choice
from .analysis import Review
import typer
import random

app = typer.Typer()


@app.command()
def preferential(people: int,
                 ring_order: int,
                 max_msg: int,
                 message_weight: int = 3,
                 initial_weight: int = 1,
                 s: float = 2.5,
                 seed: int | None = None
                 ):
    random.seed(seed)
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s)
    )
    res = simulation.simulate(ctx,
                        preferential_attachment_choice(message_weight, initial_weight),
                        seed
                        )
    print(Review(res).describe())


@app.command()
def timely(people: int,
           ring_order: int,
           max_msg: int,
           memory: int,
           message_weight: int = 3,
           initial_weight: int = 1,
           s: float = 2.5,
           seed: int | None = None
           ):
    random.seed(seed)
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s)
    )
    res = simulation.simulate(ctx,
                        timely_attachment_choice(message_weight, initial_weight, memory),
                        seed
                        )
    print(Review(res).describe())

if __name__ == '__main__':
    app()
