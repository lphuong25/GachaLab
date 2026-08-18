"""
Pulling calculation with pity system
"""
def get_pull_rate(
    base_rate,
    pull_number,
    soft_pity = 0,
    soft_rate = 0.0,
    hard_pity = 0
):
    """
    Get SSR probability for a specific pull
    """

    rate = base_rate

    # Soft pity
    if soft_pity > 0 and pull_number > soft_pity:
        rate += soft_rate * (pull_number - soft_pity)

    # Hard pity
    if hard_pity > 0 and pull_number >= hard_pity:
        rate = 1.0

    return min(max(rate, 0.0), 1.0)
