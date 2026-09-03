import pytest

from simulation import GachaGame

from simulation.fairness import(
    expected_pulls,
    expected_cost,
    worst_case_cost,
    probability_target_costs,
    analyze_game,
    normalize_lower_is_better,
    calculate_fairness_scores
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


def test_normalize_lower_is_better():

    assert normalize_lower_is_better(
        10,
        10,
        20
    ) == 100.0

    assert normalize_lower_is_better(
        20,
        10,
        20
    ) == 0.0


def test_fairness_score():

    results = [
        {
            "name": "Game A",
            "expected_cost": 50.0,
            "worst_case_cost": 100.0,
            "target_cost": {
                "50%": 50.0,
                "75%": 60.0,
                "90%": 70.0,
                "95%": 80.0
            }
        },
        {
            "name": "Game B",
            "expected_cost": 100.0,
            "worst_case_cost": 200.0,
            "target_cost": {
                "50%": 100.0,
                "75%": 120.0,
                "90%": 140.0,
                "95%": 160.0
            }
        }
    ]

    scored = calculate_fairness_scores(results)

    assert scored[0]["fairness_score"] > scored[1]["fairness_score"]