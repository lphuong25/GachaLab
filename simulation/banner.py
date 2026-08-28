from dataclasses import dataclass
import random
from .game import GachaGame
from .state import BannerState
from .result import PullResult
from .gacha import get_pull_rate

# distinct between banner featured SSR and fixed SSRs
# featured_rate is the rate to get featured character
@dataclass
class Banner:
    name: str
    featured_rate: float
    guarantee_rate: float = 0.0
    pity_carries: bool = False
    guarantee_carries: bool = False

def featured_probability (banner, guaranteed_featured = False):
    """
    Return the probability that an SSR is the featured character
    """
    if guaranteed_featured:
        return 1.0

    return banner.featured_rate

def pull(
    game: GachaGame,
    banner: Banner,
    state: BannerState,
    pull_number: int
):
    """
    Simulate one pull on a banner
    Return PullResult and update Banner State
    """

    # Calculate SSR Probability
    rate = get_pull_rate(
        base_rate=game.base_rate,
        pull_number=state.pity + 1,
        soft_pity=game.soft_pity,
        soft_rate=game.soft_rate,
        hard_pity=game.hard_pity
    )

    # Random function to determine if this pull is an SSR
    is_ssr = random.random() < rate

    # No SSR
    if not is_ssr:
        state.pity += 1

        return PullResult(
            pull_number = pull_number,
            is_ssr=False,
            is_featured=False
        )

    # SSR happened
    state.pity = 0

    # Guarantee
    if state.guaranteed_featured:

        state.guaranteed_featured = False

        return PullResult(
            pull_number = pull_number,
            is_ssr=True,
            is_featured=True
        )

    # Regular character
    is_featured = (random.random() < banner.featured_rate)

    if not is_featured:
        state.guaranteed_featured = True

    return PullResult(
        pull_number=pull_number,
        is_ssr=True,
        is_featured=is_featured
    )
