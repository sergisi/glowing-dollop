"""
Main module. Contains some scripts.

The design of the CLI is by typer. This will let us hack around more easily, which at the
end is what we want.


"""
from . import simulation, distribution, context
from .choices import preferential_attachment_choice
import typer

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
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s)
    )
    res = simulation.simulate(ctx,
                        preferential_attachment_choice(message_weight, initial_weight),
                        seed
                        )
    print(res)


@app.command()
def test(k: str):
    print(f'This is just a test: {k}')

if __name__ == '__main__':
    app()
