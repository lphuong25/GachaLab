import pytest

from simulation import GachaGame

from simulation.fairness import(
    expected_pulls,
    expected_cost,
    worst_case_cost,
    probability_target_costs,
    analyze_game
)

def test_worst_case_cost():

    game = GachaGame(
        name="Test Game",
        base_rate=0.01,
        hard_pity=100,
        cost_per_pull=2.0
    )

    assert worst_case_cost(game) == pytest.approx(200.0)

def test_expected_cost():

    game = GachaGame(
        name="Test Game",
        base_rate=1.0,
        cost_per_pull=2.0
    )

    assert expected_pulls(game) == pytest.approx(1.0)

    assert expected_cost(game) == pytest.approx(2.0)

def test_analyze_game():

    game = GachaGame(
        name="Test Game",
        base_rate=1.0,
        hard_pity=1,
        cost_per_pull=2.0
    )

    result = analyze_game(game)

    assert result["name"] == "Test Game"
    assert result["expected_pulls"] == pytest.approx(1.0)
    assert result["expected_cost"] == pytest.approx(2.0)
    assert result["worst_case_cost"] == pytest.approx(2.0)