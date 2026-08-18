import random
import numpy as np

from .gacha import get_pull_rate

def first_ssr_pull(
        base_rate,
        soft_pity = 0,
        soft_rate = 0.0,
        hard_pity = 0
):
    """
    Simulate pulls until get the first SSR
    and return pull number when get SSR"""

    pull = 0

    while True:

        pull += 1

        rate = get_pull_rate(
            base_rate = base_rate,
            pull_number = pull,
            soft_pity = soft_pity,
            soft_rate = soft_rate,
            hard_pity = hard_pity
        )

        if random.random() < rate:
            return pull

"""
Run a Monte Carlo simulation for the number
of pulls required to obtain the first ssr
"""
def monte_carlo(
        base_rate,
        simulations = 10_000,
        soft_pity = 0,
        soft_rate = 0.0,
        hard_pity = 0
):
    results = [
        first_ssr_pull(
            base_rate = base_rate,
            soft_pity = soft_pity,
            soft_rate = soft_rate,
            hard_pity = hard_pity
        )
        for _ in range(simulations)
    ]

    return {
        "mean": float(np.mean(results)),
        "median": float(np.median(results)),
        "std": float(np.std(results)),
        "results": results
    }