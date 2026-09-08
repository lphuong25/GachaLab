import pytest

from simulation import GachaGame

from simulation.analytics import (
    pulls_from_budget,
    cost_for_pulls,
    probability_from_budget,
    budget_for_probability,
    probability_from_pulls
)

def test_pulls_from_budget():

    game = GachaGame(
        name="Test Game",
        base_rate=0.01,
        cost_per_pull=2.50
    )

    assert pulls_from_budget(game, 100) == 40


def test_cost_for_pulls():

    game = GachaGame(
        name="Test Game",
        base_rate=0.01,
        cost_per_pull=2.50
    )

    assert cost_for_pulls(game, 40) == pytest.approx(100.0)


def test_probability_from_budget():

    game = GachaGame(
        name="Test Game",
        base_rate=1.0,
        cost_per_pull=2.50
    )

    probability = probability_from_budget(
        game,
        2.50
    )

    assert probability == pytest.approx(1.0)


def test_budget_for_probability():

    game = GachaGame(
        name="Test Game",
        base_rate=1.0,
        cost_per_pull=2.50
    )

    budget = budget_for_probability(
        game,
        1.0
    )

    assert budget == pytest.approx(2.50)

def test_probability_from_pulls_with_starting_pity():

    game = GachaGame(
        name="Test Game",
        base_rate=0.0,
        hard_pity=90,
        cost_per_pull=2.50
    )

    probability = probability_from_pulls(
        game,
        pulls=25,
        starting_pity=65
    )

    assert probability == pytest.approx(1.0)