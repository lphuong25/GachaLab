from .game import GachaGame
from .probability import probability_with_pity
from .gacha import get_pull_rate

def pulls_from_budget(game: GachaGame, budget: float) -> int:
    """
    Calculate number of pulls that can be purchased
    with a given budget
    """

    if budget <= 0:
        return 0

    return int(budget // game.cost_per_pull)

def cost_for_pulls(game: GachaGame, pulls: int) -> float:
    """
    Calculate cost of a given number of pull
    """

    if pulls <= 0:
        return 0.0

    return pulls * game.cost_per_pull

def probability_from_budget (game: GachaGame, budget: float) -> float:
    """
    Calculate probability to obtain at least one SSR
    within the given budget
    (return value: [0.0, 1.0])
    """

    pulls = pulls_from_budget(game, budget)

    return probability_with_pity(game, pulls)

def budget_for_probability(
        game: GachaGame, 
        target_probability: float, 
        max_budget: float = 10000.0
        ) -> float:
    """
    Find the minimum budget to reach 
    the target probability

    Probability is calculated increamentally by pull count
    """

    if target_probability <= 0:
        return 0.0

    if target_probability > 1:
        return 0.0

    max_pulls = pulls_from_budget(
        game,
        max_budget
    )

    probability_of_no_ssr = 1.0

    for pull in range(1, max_pulls + 1):
        rate = get_pull_rate(
            base_rate=game.base_rate,
            pull_number=pull,
            soft_pity=game.soft_pity,
            soft_rate=game.soft_rate,
            hard_pity=game.hard_pity
        )

        probability_of_no_ssr *= (1 - rate)

        probability = 1 - probability_of_no_ssr

        if probability >= target_probability:
            return pull * game.cost_per_pull
    return 0.0
    

def generate_budget_curve(
        game: GachaGame,
        max_budget: float = 500,
        step: float = 10
):
    """
    Generate probability for different budget levels
    """

    budgets = []
    probabilities = []

    budget = 0.0

    while budget <= max_budget:
        probability = probability_from_budget(
            game,
            budget
        )

        budgets.append(budget)
        probabilities.append(probability)

        budget += step

    return budgets, probabilities

def probability_from_pulls(
        game: GachaGame,
        pulls: int,
        starting_pity: int = 0
) -> float:
    """
    Calculate the probability of obtaining at least one SSR
    from a given number of pulls starting at a given pity
    """

    if pulls <= 0:
        return 0.0

    return probability_with_pity(
        game, 
        pulls,
        starting_pity=starting_pity
    )