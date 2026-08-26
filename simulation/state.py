# This will calculate the player's gacha state
from dataclasses import dataclass

# Get the number of unsucessful rolls as pity
@dataclass
class BannerState:
    pity: int = 0
    guaranteed_featured: bool = False
