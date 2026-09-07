import streamlit as st
import pandas as pd
import plotly.express as px

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

from simulation.probability import (
    probability_with_pity,
    generate_probability_curve)

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
st.header("Pulling Budget")

# Add saved pull and calculate it with the purchased ones
saved_pulls = st.slider(
    "How many pulls have you already saved?",
    min_value=0,
    max_value=1000,
    value=0,
    step=1
)

budget = st.slider(
    "How much are you willing to spend?",
    min_value = 0.0,
    max_value = 1000.0,
    value = 100.0,
    step = 5.0
)

paid_pulls = pulls_from_budget(
    selected_game,
    budget
)

total_pulls = saved_pulls + paid_pulls

probability = probability_with_pity(
    selected_game,
    total_pulls
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Saved Pulls", saved_pulls
)

col2.metric(
    "Paid Pulls", paid_pulls
)

col3.metric(
    "Total Pulls", total_pulls
)
st.metric(
    "SSR Probability", f"{probability: .2%}"
)

# Hard pity information
if selected_game.hard_pity > 0:

    pulls_to_pity = max(
        selected_game.hard_pity - total_pulls,
        0
    )

    cost_to_pity = pulls_to_pity * selected_game.cost_per_pull

    if pulls_to_pity == 0:
        st.success(
            "🎉 You have reached the hard pity threshold!"
        )
    else:
        st.info(
            f"You are {pulls_to_pity} pulls away "
            f"from hard pity."
        )

        st.write(
            f"Estimated additional cost to reach hard pity: "
            f"**${cost_to_pity:.2f}**"
        )

else:

    st.info(
        "This game does not have a hard pity value "
        "in the current dataset."
    )

# Progress bar
if selected_game.hard_pity > 0:

    pity_progress = min(
        total_pulls / selected_game.hard_pity,
        1.0
    )

    st.progress(
        pity_progress,
        text=f"Pity Progress: {total_pulls} / {selected_game.hard_pity}"
    )

with st.expander("How does Pulling Budget work?"):

    st.write(
        """
        Pulling Budget combines pulls you have already saved
        with pulls you purchase from your budget.

        Total Pulls = Saved Pulls + Paid Pulls

        The resulting total is then used to calculate your
        probability of obtaining at least one SSR.

        If the game has a hard pity system, GachaLab also
        calculates how many additional pulls and how much
        money would be required to reach the hard pity threshold.
        """
    )

# Probability verdict message
if probability >= 0.90:
    st.success(
        f"With ${budget:.2f}, you have a {probability:.1%} chance "
        f"of getting at least one SSR"
    )

elif probability >= 0.50:
    st.warning(
        f"With ${budget:.2f}, you have a {probability:.1%} chance "
        f"of getting at least one SSR"
    )
else:
    st.error(
        f"With ${budget:.2f}, you only have a {probability:.1%} chance "
        f"of getting at least one SSR"        
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
    "The GachaLab Fairness Score measures how favorable a game's "
    "gacha system is relative to the other games in the dataset. "
    "Lower costs receive higher scores."
)

with st.expander("How is the Fairness Score calculated?"):
    st.write("""
    The Fairness Score is based on three factors:

    • Expected Cost = 40%
    
    How much a player is expected to spend to obtain an SSR.

    • 90% Success Cost = 40%
    
    How much a player needs to spend to have a 90% chance of
    obtaining at least one SSR.

    • Worst-Case Cost = 20%
    
    The maximum amount a player would need to spend before
    reaching the hard pity guarantee.

    Lower costs result in higher scores.
    """)

# display components
st.subheader("Fairness Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Expected Cost",
    f"${selected_result['expected_cost']:.2f}"
)

col2.metric(
    "Cost for 90% Chance",
    f"${selected_result['target_cost']['90%']:.2f}"
)

if selected_result["worst_case_cost"] is not None:
    col3.metric(
        "Worst-Case Cost",
        f"${selected_result['worst_case_cost']:.2f}"
    )
else:
    col3.metric(
        "Worst-Case Cost",
        "No hard pity"
    )

# Generate probability chart 
st.header("SSR Probability by Pulls")

pulls, probabilities = generate_probability_curve(
    selected_game,
    max_pulls=selected_game.hard_pity
        if selected_game.hard_pity > 0 
        else 300,
    step = 1
)

probability_df = pd.DataFrame({
    "Pulls": pulls,
    "SSR Probability": probabilities
})

fig = px.line(
    probability_df,
    x="Pulls",
    y="SSR Probability",
    title=f"{selected_game.name}'s SSR Probability"
)

# Adding horizontal reference lines for each threshold
fig.add_hline(
    y=0.50,
    line_dash="dash",
    line_color="red",
    annotation_text="50%"
)

fig.add_hline(
    y=0.75,
    line_dash="dash",
    line_color="red",
    annotation_text="75%"
)

fig.add_hline(
    y=0.90,
    line_dash="dash",
    line_color="red",
    annotation_text="90%"
)

fig.add_hline(
    y=0.95,
    line_dash="dash",
    line_color="red",
    annotation_text="95%"
)

fig.update_yaxes(
    tickformat = ".0%",
    range = [0, 1]
)

fig.update_layout(
    xaxis_title = "Number of Pulls",
    yaxis_title = "Probability of at least one SSR"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# Cost of reaching each threshold
st.header("Cost to Reach an SSR Probability")

selected_result = next(
    result for result in scored_results
    if result["name"] == selected_game.name
)

target_costs = selected_result["target_cost"]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "50% Chance", f"${target_costs['50%']:.2f}"
)

col2.metric(
    "75% Chance", f"${target_costs['75%']:.2f}"
)

col3.metric(
    "90% Chance", f"${target_costs['90%']:.2f}"
)

col4.metric(
    "95% Chance", f"${target_costs['95%']:.2f}"
)

# Game comparision chart
st.header("Fairness Comparision")

show_games = st.multiselect(
    "Compare games",
    game_names,
    default=game_names
)

comparison_df = pd.DataFrame([
    {
        "Game": result["name"],
        "Fairness Score": result["fairness_score"]
    }
    for result in scored_results
    if result["name"] in show_games
])

comparison_df = comparison_df.sort_values(
    "Fairness Score",
    ascending=True
)

fig_comparision = px.bar(
    comparison_df,
    x="Fairness Score",
    y="Game",
    orientation="h",
    title="GachaLab Fairness Score by Game"
)

fig_comparision.update_xaxes(
    range=[0, 100]
)

fig_comparision.update_layout(
    xaxis_title = "Fairness Score",
    yaxis_title="Game"
)

st.plotly_chart(
    fig_comparision,
    use_container_width=True
)

score = selected_result["fairness_score"]

# Verdict
if score >= 80:
    verdict = "🟢 Relatively Favorable"
    explanation = (
        "This game scores relatively well compared with the "
        "other games analyzed by GachaLab."
    )
elif score >= 60:
    verdict = "🟡 Average"
    explanation = (
        "This game's gacha system falls around the middle "
        "of the games analyzed by GachaLab."
    )
elif score >= 40:
    verdict = "🟠 Relatively Expensive"
    explanation = (
        "This game's gacha system is less favorable compared "
        "with the other games analyzed."
    )
else:
    verdict = "🔴 Very Expensive"
    explanation = (
        "This game has relatively high acquisition costs "
        "compared with the other games analyzed."
    )

st.subheader(f"Verdict: {verdict}")
st.write(explanation)

# Add ranking table
st.subheader("Fairness Ranking")

ranking_df = pd.DataFrame([
    {
        "Rank": index + 1,
        "Game": result["name"],
        "Fairness Score": result["fairness_score"],
        "Expected Cost": result["expected_cost"],
        "90% Success Cost": result["target_cost"]["90%"],
        "Worst-Case Cost": result["worst_case_cost"]
    }
    for index, result in enumerate(
        sorted(
            scored_results,
            key=lambda x: x["fairness_score"],
            reverse=True
        )
    )
])

st.dataframe(
    ranking_df,
    use_container_width=True,
    hide_index=True
)

