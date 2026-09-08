
from .game import GachaGame
from .gacha import get_pull_rate

"""
Mathematical probability calculate
the probability will change on every pull
"""
def probability_at_least_one(rate, pulls): 

    if pulls <= 0:
        return 0.0
    if rate <= 0:
        return 0.0
    if rate >= 1:
        return 1.0

    probability_of_no_success = (1 - rate) ** pulls
    return 1 - probability_of_no_success


"""
Mathematical probability calculate 
the rate with pity system to get 
at least 1 SSR within total_pulls,
stating from a given pity count
"""
def probability_with_pity(
        game: GachaGame,
        total_pulls: int,
        starting_pity: int = 0
):

    if total_pulls <= 0:
        return 0.0

    if starting_pity < 0:
        starting_pity = 0

    probability_of_no_ssr = 1.0

    for pull in range(1, total_pulls + 1):

        current_pity = starting_pity + pull

        rate = get_pull_rate(
            base_rate=game.base_rate,
            pull_number=current_pity,
            soft_pity=game.soft_pity,
            soft_rate=game.soft_rate,
            hard_pity=game.hard_pity
        )

        probability_of_no_ssr *= (1 - rate)

    return 1 - probability_of_no_ssr

def generate_probability_curve (
        game: GachaGame,
        max_pulls: int,
        step: int = 1,
        starting_pity: int = 0
):
    """
    Generate SSR probability for a range of pulls
    
    This calculate the probability incrementally instead of
    recalculate the entire probability for every pull
    """

    pulls = []
    probabilities = []

    probability_of_no_ssr = 1.0

    for total_pulls in range(0, max_pulls + 1):

        if total_pulls == 0:
            probability = 0.0

        else:
            current_pity = starting_pity + total_pulls

            rate = get_pull_rate(
                base_rate=game.base_rate,
                pull_number=current_pity,
                soft_pity=game.soft_pity,
                soft_rate=game.soft_rate,
                hard_pity=game.hard_pity
            )

            probability_of_no_ssr *= (1 - rate)

            probability = 1 - probability_of_no_ssr

        if total_pulls % step == 0:
            pulls.append(total_pulls)
            probabilities.append(probability)

    return pulls, probabilities

