from data.data_loader import load_games
from simulation.fairness import (
    analyze_all,
    calculate_fairness_scores
)

games = load_games("data/gachagame.xlsx")

results = analyze_all(games)

scored_results = calculate_fairness_scores(results)

for result in scored_results:
    print(
        result["name"],
        "->",
        "Expected:", result["expected_cost_score"],
        "| 90%:", result["90_percent_score"],
        "| Worst:", result["worst_case_score"],
        "| Fairness:", result["fairness_score"]
    )