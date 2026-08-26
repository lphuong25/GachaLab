import random
import numpy as np

from .game import GachaGame
from .gacha import get_pull_rate

def first_ssr_pull(game: GachaGame):
    """
    Simulate pulls until get the first SSR
    and return pull number when get SSR"""

    pull = 0

    while True:

        pull += 1

        rate = get_pull_rate(
            base_rate = game.base_rate,
            pull_number = pull,
            soft_pity = game.soft_pity,
            soft_rate = game.soft_rate,
            hard_pity = game.hard_pity
        )

        if random.random() < rate:
            return pull

"""
Run a Monte Carlo simulation for the number
of pulls required to obtain the first ssr
"""
def monte_carlo(
        game: GachaGame,
        simulations = 10_000
):
    results = [
        first_ssr_pull(game)
        for _ in range(simulations)
    ]

    return {
        "mean": float(np.mean(results)),
        "median": float(np.median(results)),
        "std": float(np.std(results)),
        "results": results
    }