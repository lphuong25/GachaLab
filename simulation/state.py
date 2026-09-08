# This will calculate the player's gacha state
from dataclasses import dataclass

# Get the number of unsucessful rolls as pity
@dataclass
class BannerState:
    pity: int = 0
    guaranteed_featured: bool = False

    # Reset pity when SSR appear
    def reset_pity(self):
        self.pity = 0

def pulls_until_pity(
        state: BannerState, 
        hard_pity: int) -> int | None:
    """
    Calculate how many pulls needed for hard pity
    
    Return None if the game doesn't have hard pity system"""

    if hard_pity <= 0:
        return None

    return max(hard_pity - state.pity, 0)
