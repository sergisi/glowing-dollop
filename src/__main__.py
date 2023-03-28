"""
Main module. Contains some scripts.

The design of the CLI is by typer. This will let us hack around more easily, which at the
end is what we want.


"""
from . import simulation, distribution, context
from .choices import (
    preferential_attachment_choice,
    timely_attachment_choice,
    randomly_attachment_choice,
)
from .analysis import Review, anonymity_window, anonymity_score, SplitReview
import typer
import random

app = typer.Typer()


def _preferential(
    people: int,
    ring_order: int,
    max_msg: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    seed: int | None = None,
) -> simulation.Simulation:
    """
    Leverages preferential analysis. Returns the simulation to perform the reports.
    """
    random.seed(seed)
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s),
    )
    res = simulation.simulate(
        ctx, preferential_attachment_choice(message_weight, initial_weight), seed
    )
    return res


@app.command()
def preferential(
    people: int,
    ring_order: int,
    max_msg: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    first_quantile: float = 0.05,
    second_quantile: float = 0.75,
    seed: int | None = None,
    headers: bool = True,
):
    """
        Preferential attachment simulation. This simulation weights all the messages. It reports the user-data
        in total and with two different quartiles.
    """
    res = _preferential(
        people, ring_order, max_msg, message_weight, initial_weight, s, seed
    )
    if headers:
        _print_headers()
    _print_description(res, first_quantile, second_quantile, 'preferential')


@app.command()
def csv_preferential(
    people: int,
    ring_order: int,
    max_msg: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    seed: int | None = None,
):
    """
        Preferential attachment simulation. Returns all the data of the users in a csv, printed in the
        stdout.
    """
    res = _preferential(
        people, ring_order, max_msg, message_weight, initial_weight, s, seed
    )
    r = Review(res, anonymity_score(res))
    print(r.to_csv())


def _window(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    seed: int | None = None,
) -> simulation.Simulation:
    """
        Window simulation utils. Just to output more numbers.
    """
    random.seed(seed)
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s),
    )
    res = simulation.simulate(
        ctx, timely_attachment_choice(message_weight, initial_weight, memory), seed
    )

    return res


def _print_headers():
    print(
        "| "
        + " | ".join(
            [
                "reviewer",
                "anonymity",
                "medium dev",
                "mean",
                "min",
                "q0.25",
                "median",
                "q0.75",
                "max",
                "#messages",
                "#signatures",
            ]
        )
        + " |"
    )


def _print_description(res: simulation.Simulation,
                       first_quantile,
                       second_quantile,
                       pref='normal',
                       user_list=None):
    """
        Prints a description of the users.
    """
    if user_list == None:
        user_list = anonymity_score(res)
    r = Review(res, user_list)
    print(f"| {pref} | " + r.describe() + " |")
    r = SplitReview(res, user_list, first_quantile, second_quantile)
    print(r.describe())


@app.command()
def window(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    first_quantile: float = 0.05,
    second_quantile: float = 0.75,
    seed: int | None = None,
):
    """
    Analysis a window attachmment. It prints two adjancent tables, one for the first mesage
    anonymity and the other for the global messages.
    """
    res = _window(
        people, ring_order, max_msg, memory, message_weight, initial_weight, s, seed
    )
    _print_headers()
    user_list = anonymity_window(memory)(res)
    _print_description(res, first_quantile, second_quantile, 'first-message', user_list)
    _print_description(res, first_quantile, second_quantile, 'window')


@app.command()
def report(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    preferential_message_weight: int = 3,
    preferential_initial_weight: int = 1,
    s: float = 2.5,
    first_quantile: float = 0.05,
    second_quantile: float = 0.75,
    seed: int | None = None,
):
    """
        Util to create both a report of a window attachment and preferential attachment. It can change the
        parameters accordingly so they are tailored for both algorithms.
    """
    random.seed(seed)
    window(
        people,
        ring_order,
        max_msg,
        memory,
        message_weight,
        initial_weight,
        s,
        first_quantile,
        second_quantile,
        None,
    )
    print("|-")
    preferential(
        people,
        ring_order,
        max_msg,
        preferential_message_weight,
        preferential_initial_weight,
        s,
        first_quantile,
        second_quantile,
        None,
        False,
    )


@app.command()
def csv_window(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    message_weight: int = 3,
    initial_weight: int = 1,
    s: float = 2.5,
    seed: int | None = None,
    mode: str = "all",
):
    assert mode in ["all", "window"]
    modes = {
        "all": lambda r: Review(r, anonymity_score(r)),
        "window": lambda r: Review(r, anonymity_window(memory)(r)),
    }
    r = _window(
        people, ring_order, max_msg, memory, message_weight, initial_weight, s, seed
    )
    r = modes[mode](r)
    print(r.to_csv())


def _randomly(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    s: float = 2.5,
    seed: int | None = None,
):
    random.seed(seed)
    ctx = context.Context(
        people=people,
        ring_order=ring_order,
        distribution=distribution.zipf_distribution(max_msg, s),
    )
    res = simulation.simulate(ctx, randomly_attachment_choice(memory), seed)
    return Review(res, anonymity_score(res))


@app.command()
def randomly(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    s: float = 2.5,
    seed: int | None = None,
):
    r = _randomly(people, ring_order, max_msg, memory, s, seed)
    print(r.describe())


@app.command()
def csv_randomly(
    people: int,
    ring_order: int,
    max_msg: int,
    memory: int,
    s: float = 2.5,
    seed: int | None = None,
):
    r = _randomly(people, ring_order, max_msg, memory, s, seed)
    print(r.to_csv())


@app.command()
def test(
    command: str,
    tries: int = 100,
    message_weight: int = 3,
    initial_weight: int = 1,
    window: int = 20,
    max_msg: int = 100,
    s: float = 1.2,
):
    assert command in ["window", "randomly", "pref"]
    attachments = {
        "window": timely_attachment_choice(message_weight, initial_weight, window),
        "randomly": randomly_attachment_choice(window),
        "pref": preferential_attachment_choice(message_weight, initial_weight),
    }
    attachment = attachments[command]
    res = []
    ctx = context.Context(
        people=400, ring_order=8, distribution=distribution.zipf_distribution(100, 1.2)
    )
    for seed in range(tries):
        random.seed(seed)
        res = simulation.simulate(ctx, attachment, seed)
        r = Review(res, anonymity_score(res))
        if r.anonymity > 0:
            res.append((seed, r.anonymity))

    print(f"{command}: {res}")
    print(f"{command}: Number of times: {len(res)} out of {tries=}")
    return len(res)


if __name__ == "__main__":
    app()
