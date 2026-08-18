import pytest
from simulation import (
    probability_at_least_one,
    probability_with_pity,
    get_pull_rate,
    first_ssr_pull,
    monte_carlo,
    GachaGame
)

def test_basic_probability():
    probability = probability_at_least_one(
        rate = 0.01,
        pulls = 1
    )

    assert probability == pytest.approx(0.01)

def test_no_pulls():
    probability = probability_at_least_one(
        rate = 0.01,
        pulls = 0
    )

    assert probability == pytest.approx(0.0)

def test_guaranteed_pull():

    probability = probability_with_pity(
        base_rate=0.01,
        total_pulls=1,
        hard_pity=1
    )

    assert probability == pytest.approx(1.0)

def test_genshin_hard_pity():
    # Before soft pity
    assert get_pull_rate(
        base_rate=0.006,
        pull_number=74,
        soft_pity=74,
        soft_rate=0.06,
        hard_pity=90
    ) == pytest.approx(0.006)

    # First pull after soft pity
    assert get_pull_rate(
        base_rate=0.006,
        pull_number=75,
        soft_pity=74,
        soft_rate=0.06,
        hard_pity=90
    ) == pytest.approx(0.066)

    # Hard pity
    assert get_pull_rate(
        base_rate=0.006,
        pull_number=90,
        soft_pity=74,
        soft_rate=0.06,
        hard_pity=90
    ) == pytest.approx(1.0)

# Simplest test
def test_first_ssr_with_guaranteed_pull():
    result = first_ssr_pull(
        base_rate = 0.0,
        hard_pity = 1
    )
    assert result == 1

# Hard pity: Simulate 1000 players and ensure they will get ssr at least at 90 pulls
def test_first_ssr_never_exceed_hard_pity():
    result = [
        first_ssr_pull (
            base_rate=0.006,
            soft_pity=74,
            soft_rate=0.06,
            hard_pity=90
        )
        for _ in range(1000)
    ]
    assert max(result) <= 90

# Monte Carlo
def test_monte_carlo_result_size():
    stats = monte_carlo(
        base_rate=0.01,
        simulations=1000
    )
    assert len(stats["results"]) == 1000

# Test Monte Carlo return statistic
def test_monte_carlo_return_statistic():
    stats = monte_carlo(
        base_rate=0.01,
        simulations=1000
    )
    assert stats["mean"] > 0
    assert stats["median"] > 0
    assert stats["std"] >= 0

def test_monte_carlo_mean():
    stats = monte_carlo(
        base_rate=0.01,
        simulations=100_000
    )

    assert stats["mean"] == pytest.approx(
        100,
        abs=1.0
    )

# Test dataclass
def test_gacha_game():
    game = GachaGame(
        name="Genshin Impact",
        base_rate=0.006,
        soft_pity=74,
        soft_rate=0.06,
        hard_pity=90,
        cost_per_pull=2.64
    )

    assert game.name == "Genshin Impact"
    assert game.base_rate == pytest.approx(0.006)
    assert game.soft_pity == 74
    assert game.hard_pity == 90
    assert game.cost_per_pull == pytest.approx(2.64)