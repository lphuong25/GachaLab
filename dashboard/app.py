import streamlit as st
import pandas as pd

from data.data_loader import load_games
from simulation.analytics import (
    pulls_from_budget,
    probability_from_budget,
    budget_for_probability
)

from simulation.fairness import (
    analyze_all,
    calculate_fairness_scores
)

# Page configuration
st.set_page_config(
    page_title="GachaLab",
    layout="wide"
)

# Load data
games = load_games("data/gachagame.xlsx")

results = analyze_all(games)
scored_results = calculate_fairness_scores(results)

# Title
st.title("GachaLab")
st.subheader("Is this Gacha Game actually fair?")
st.write(
    "Analyze gacha systems using probability, " \
    "including pity system, expected cost, and standarize Fairness Score"
)

# Game Selection option
st.sidebar.header("Game Selection")

game_names = [game.name for game in games]

selected_name = st.sidebar.selectbox(
    "Choose a game",
    game_names
)

selected_game = next(
    game for game in games
    if game.name == selected_name
)

# Basic game information
st.header(selected_game.name)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Base SSR Rate",
    f"{selected_game.base_rate: .2%}"
)

col2.metric(
    "Soft Pity",
    selected_game.soft_pity
)

col3.metric(
    "Hard Pity",
    selected_game.hard_pity
)

col4.metric(
    "Cost/Pull",
    f"${selected_game.cost_per_pull: .2f}"
)

# Add budget
st.header("Budget analysis")

budget = st.slider(
    "How much are you willing to spend?",
    min_value = 0.0,
    max_value = 1000.0,
    value = 100.0,
    step = 5.0
)

pulls = pulls_from_budget(
    selected_game,
    budget
)

probability = probability_from_budget(
    selected_game,
    budget
)

col1, col2 = st.columns(2)

col1.metric(
    "Pulls",
    pulls
)

col2.metric(
    "SSR Probability",
    f"{probability: .2%}"
)

# Show Fairness Score
selected_result = next(
    result
    for result in scored_results
    if result["name"] == selected_game.name
)

st.header("GachaLab Fairness Score")

st.metric(
    "Fairness Score",
    f"{selected_result['fairness_score']: .2f} / 100"
)

st.write(
    "The score combines expected cost, 90% sucess cost, " \
    "and worst-case cost"
)

# display components
col1, col2, col3 = st.columns(3)

col1.metric(
    "Expected Cost Score",
    f"{selected_result['expected_cost_score']: .2f}"
)

col2.metric(
    "90% Sucess Score",
    f"{selected_result['90_percent_score']: .2f}"
)

col3.metric(
    "Worst-case Score",
    f"{selected_result['worst_case_score']: .2f}"
)
