from dataclasses import dataclass

# distinct between banner featured SSR and fixed SSRs
# featured_rate is the rate to get featured character
@dataclass
class Banner:
    name: str
    featured_rate: float
    guarantee_rate: float = 0.0
    pity_carries: bool = False
    guarantee_carries: bool = False