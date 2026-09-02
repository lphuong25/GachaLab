from .game import GachaGame
from .probability import probability_with_pity
from .analytics import budget_for_probability

"""
Calculate expected number of pulls 
instead of relying only on percentage
"""
def expected_pulls(
        game: GachaGame,
        max_pulls: int = 1000
) -> float:
    """
    Calculate the expected number of pulls for at least 1 SSR
    """
    expected = 0.0

    for pull in range(1, max_pulls + 1):
        probability_before = probability_with_pity(
            game,
            pull - 1
        )

        probability_at_pull = probability_with_pity(
            game,
            pull
        )
        probability_exact = (probability_at_pull - probability_before)

        expected += (pull * probability_exact)

    return expected

def expected_cost(game: GachaGame) -> float:
    """
    Extimate the expected money cost to
    obtain an SSR
    """

    pulls = expected_pulls(game)

    return pulls * game.cost_per_pull

def worst_case_cost(game: GachaGame) -> float | None:
    """
    Calculate the cost to reach hard pity
    """

    if game.hard_pity <= 0:
        return None

    return game.hard_pity * game.cost_per_pull

def probability_target_costs(
        game: GachaGame
) -> dict:
    """
    Calculate the approximate cost require to 
    reach certain checkpoints
    """

    targets = {
        "50%": 0.50,
        "75%": 0.75,
        "90%": 0.90,
        "95%": 0.95
    }

    results = {}

    for label, target in targets.items():
        results[label] = budget_for_probability(
            game,
            target
        )

    return results

# Combine all functions
def analyze_game(game: GachaGame) -> dict:
    """
    A complete fairness analyze report
    """

    expected = expected_pulls(game)
    target_costs = probability_target_costs(game)


    worst_case = worst_case_cost(game)

    return {
        "name": game.name,
        "base_rate": game.base_rate,
        "expected_pulls": round(expected, 2),
        "expected_cost": round(expected * game.cost_per_pull, 2),
        "worst_case_cost": round(worst_case, 2) if worst_case is not None else None,
        "target_cost": {
            key: round(value, 2)
            for key, value in target_costs.items()
        }
    }

def analyze_all(games):
    """
    Give an analyze for all games in the dataset
    """
    return [
        analyze_game(game)
        for game in games
    ]