from dataclasses import dataclass

@dataclass
class GachaGame:
    name: str
    base_rate: float
    soft_pity: int = 0
    soft_rate: float = 0.0
    hard_pity: int = 0
    cost_per_pull: float = 0.0
