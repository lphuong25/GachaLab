from .game import GachaGame
from .gacha import get_pull_rate
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
    
    This calculate the probability distribution
    incrementally to avoid repeated probability calculations
    """
    expected = 0.0
    probability_of_no_ssr = 1.0

    for pull in range(1, max_pulls + 1):

        rate = get_pull_rate(
            base_rate=game.base_rate,
            pull_number=pull,
            soft_pity=game.soft_pity,
            soft_rate=game.soft_rate,
            hard_pity=game.hard_pity
        )

        probability_exact = (probability_of_no_ssr * rate)

        expected += (pull * probability_exact)

        # Update probability if not having SSR
        probability_of_no_ssr *= (1- rate)

        # Obtain SSR then no additional pulls matter
        if probability_of_no_ssr == 0:
            break

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

# Build Fairness Index
def normalize_lower_is_better(value, min_value, max_value):
    if max_value == min_value:
        return 100.0

    return (max_value - value) / (max_value - min_value) * 100.0

def calculate_fairness_scores(results):
    """
    Calculate 0-100 Fairness Score
    
    Lower expected cost, 90% success cost,
    and worst-case cost are considered better.

    The scoring system is the sum of 40% expected cost,
    40% of 90% success rate and 20% of worst case
    """
    expected_costs = [
        result["expected_cost"]
        for result in results
    ]

    target_90_costs = [
        result["target_cost"]["90%"]
        for result in results
    ]

    worst_case_costs = [
        result["worst_case_cost"]
        for result in results
        if result["worst_case_cost"] is not None
    ]

    min_expected = min(expected_costs)
    max_expected = max(expected_costs)

    min_90 = min(target_90_costs)
    max_90 = max(target_90_costs)

    min_worst = min(worst_case_costs)
    max_worst = max(worst_case_costs)

    scored_results = []

    for result in results:
        expected_score = normalize_lower_is_better(
            result["expected_cost"],
            min_expected,
            max_expected
        )
        target_90_score = normalize_lower_is_better(
            result["target_cost"]["90%"],
            min_90,
            max_90
        )

        if result["worst_case_cost"] is not None:
            worst_score = normalize_lower_is_better(
                result["worst_case_cost"],
                min_worst,
                max_worst
            )
        else:
            worst_score = 0.0

        fairness_score = (
            expected_score * 0.40
            + target_90_score * 0.40
            + worst_score * 0.20
        )

        scored_result = result.copy()

        scored_result["expected_cost_score"] = round(expected_score, 2)

        scored_result["90_percent_score"] = round(target_90_score, 2)

        scored_result["worst_case_score"] = round(worst_score, 2)       

        scored_result["fairness_score"] = round(fairness_score, 2)    

        scored_results.append(scored_result)

    return scored_results 