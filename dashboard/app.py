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
    generate_probability_curve
)

from simulation.state import pulls_until_pity

# Page configuration
st.set_page_config(
    page_title="GachaLab",
    layout="wide"
)

# Load data
games = load_games("data/gachagame.xlsx")

results = analyze_all(games)
scored_results = calculate_fairness_scores(results)

# ============================================================
# Dashboard Header
# ============================================================

st.title("GachaLab")
st.markdown("### Is this gacha actually fair?")

st.write(
    "Explore how probability, pity systems, and spending affect "
    "your chances of obtaining an SSR."
)

# Game Selection
game_names = [game.name for game in games]

selected_name = st.selectbox(
    "Select a game",
    game_names
)

selected_game = next(
    game for game in games
    if game.name == selected_name
)

st.divider()


# ============================================================
# Game Snapshot
# ============================================================

st.subheader("Game Snapshot")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Base SSR Rate",
    f"{selected_game.base_rate:.2%}"
)

col2.metric(
    "Soft Pity",
    (
        f"{selected_game.soft_pity} pulls"
        if selected_game.soft_pity > 0
        else "None"
    )
)

col3.metric(
    "Hard Pity",
    (
        f"{selected_game.hard_pity} pulls"
        if selected_game.hard_pity > 0
        else "None"
    )
)

col4.metric(
    "Cost / Pull",
    f"${selected_game.cost_per_pull:.2f}"
)

st.divider()


# ============================================================
# Pull Planner
# ============================================================

st.subheader("Plan Your Pulls")

st.write(
    "Enter the pulls you already have, your current pity, and "
    "your spending budget to estimate your chance of obtaining "
    "at least one SSR."
)

col1, col2, col3 = st.columns(3)

with col1:
    saved_pulls = st.slider(
        "Saved pulls",
        min_value=0,
        max_value=500,
        value=0,
        step=1,
        help="Pulls you already have available before spending more money."
    )

with col2:
    current_pity = st.slider(
        "Current pity",
        min_value=0,
        max_value=(
            selected_game.hard_pity
            if selected_game.hard_pity > 0
            else 1000
        ),
        value=0,
        step=1,
        help="Your current pity counter before starting your planned pulls."
    )

with col3:
    budget = st.slider(
        "Spending budget",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        step=5.0,
        help="How much additional money you are willing to spend."
    )


# Calculate planned pulls
paid_pulls = pulls_from_budget(
    selected_game,
    budget
)

total_pulls = saved_pulls + paid_pulls

probability = probability_with_pity(
    selected_game,
    total_pulls,
    starting_pity=current_pity
)


# ============================================================
# Pull Plan Summary
# ============================================================

st.markdown("#### Your Pull Plan")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Saved Pulls",
    saved_pulls
)

col2.metric(
    "Paid Pulls",
    paid_pulls
)

col3.metric(
    "Total Planned Pulls",
    total_pulls
)


# ============================================================
# SSR Probability
# ============================================================

st.markdown("#### Your SSR Chance")

st.metric(
    "Chance of getting at least one SSR",
    f"{probability:.1%}"
)

if probability >= 0.90:
    st.success(
        f"🟢 High chance — your planned pulls give you a "
        f"{probability:.1%} chance of obtaining at least one SSR."
    )

elif probability >= 0.50:
    st.warning(
        f"🟡 Moderate chance — your planned pulls give you a "
        f"{probability:.1%} chance of obtaining at least one SSR."
    )

else:
    st.error(
        f"🔴 Low chance — your planned pulls give you only a "
        f"{probability:.1%} chance of obtaining at least one SSR."
    )


# ============================================================
# Pity Progress
# ============================================================

if selected_game.hard_pity > 0:

    # This represents maximum pity progress if no SSR is obtained.
    current_pity_after_pulls = current_pity + total_pulls

    pulls_to_pity = max(
        selected_game.hard_pity - current_pity_after_pulls,
        0
    )

    cost_to_pity = pulls_to_pity * selected_game.cost_per_pull

    st.markdown("#### Pity Progress")

    pity_progress = min(
        current_pity_after_pulls / selected_game.hard_pity,
        1.0
    )

    st.progress(
        pity_progress,
        text=(
            f"{min(current_pity_after_pulls, selected_game.hard_pity)} "
            f"/ {selected_game.hard_pity} pulls"
        )
    )

    if pulls_to_pity == 0:
        st.success(
            "🎉 Your planned pulls can reach the hard pity threshold "
            "if no SSR is obtained first."
        )
    else:

        col1, col2 = st.columns(2)

        col1.metric(
            "Pulls Until Hard Pity",
            pulls_to_pity
        )

        col2.metric(
            "Additional Cost to Reach Pity",
            f"${cost_to_pity:.2f}"
        )

else:

    st.info(
        "This game does not have a hard pity value "
        "in the current dataset."
    )


# ============================================================
# Pull Planner Explanation
# ============================================================

with st.expander("How does the Pull Planner work?"):

    st.write(
        """
        **Saved pulls** are pulls you already have available.

        **Paid pulls** are the number of pulls your spending budget
        can purchase based on the game's cost per pull.

        **Total planned pulls** are calculated as:

        **Saved Pulls + Paid Pulls**

        GachaLab then uses your total planned pulls and current pity
        to estimate your probability of obtaining at least one SSR.

        Pity progress shows the maximum pity you could reach if you
        do not obtain an SSR before reaching the hard pity threshold.
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

# ============================================================
# Fairness Score
# ============================================================

st.divider()

st.subheader("Is This Gacha Fair?")

fairness_score = selected_result["fairness_score"]

# Determine a simple interpretation of the score
if fairness_score >= 80:
    fairness_label = "Relatively Favorable"
    fairness_message = (
        "This game scores relatively well compared with "
        "the other games in the GachaLab dataset."
    )
elif fairness_score >= 60:
    fairness_label = "Moderate"
    fairness_message = (
        "This game falls around the middle of the games "
        "analyzed by GachaLab."
    )
else:
    fairness_label = "Relatively Expensive"
    fairness_message = (
        "This game scores relatively poorly compared with "
        "the other games in the GachaLab dataset."
    )


# Main score
col1, col2 = st.columns([1, 2])

with col1:
    st.metric(
        "GachaLab Fairness Score",
        f"{fairness_score:.1f} / 100"
    )

with col2:
    st.markdown(f"### {fairness_label}")
    st.write(fairness_message)


# ------------------------------------------------------------
# Fairness Metrics
# ------------------------------------------------------------

st.markdown("#### What Drives the Score?")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Expected Cost",
        f"${selected_result['expected_cost']:.2f}"
    )

with col2:
    target_90_cost = selected_result["target_cost"]["90%"]

    st.metric(
        "Cost for 90% Chance",
        f"${target_90_cost:.2f}"
    )

with col3:
    worst_case = selected_result["worst_case_cost"]

    if worst_case is None:
        st.metric(
            "Worst-Case Cost",
            "No hard pity"
        )
    else:
        st.metric(
            "Worst-Case Cost",
            f"${worst_case:.2f}"
        )


# ------------------------------------------------------------
# Score Explanation
# ------------------------------------------------------------

with st.expander("How is the Fairness Score calculated?"):

    st.write(
        """
        The GachaLab Fairness Score is a relative score that compares
        gacha systems across the games in the current dataset.

        A lower estimated cost receives a higher score.

        The score currently considers three factors:
        """
    )

    st.markdown(
        """
        - **Expected Cost — 40%**  
          Estimated spending required to obtain an SSR on average.

        - **90% Success Cost — 40%**  
          Estimated spending required to reach a 90% chance of
          obtaining at least one SSR.

        - **Worst-Case Cost — 20%**  
          Maximum spending required to reach hard pity, when the
          game has a hard pity system.
        """
    )

    st.info(
        "The Fairness Score is relative to the games and assumptions "
        "in GachaLab's dataset. It is not an objective measure of "
        "whether a game is universally fair or unfair."
    )

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

# ============================================================
# Probability Analysis
# ============================================================

st.divider()

st.subheader("Probability Analysis")

st.write(
    "See how your chance of obtaining at least one SSR changes "
    "as you make more pulls."
)

max_pulls = (
    selected_game.hard_pity
    if selected_game.hard_pity > 0
    else 300
)

pulls, probabilities = generate_probability_curve(
    selected_game,
    max_pulls=max_pulls,
    step=1
)


# ------------------------------------------------------------
# Find Pull Thresholds
# ------------------------------------------------------------

thresholds = {
    "50% Chance": 0.50,
    "75% Chance": 0.75,
    "90% Chance": 0.90,
    "95% Chance": 0.95
}

threshold_pulls = {}

for label, target in thresholds.items():

    required_pulls = None

    for pull, probability_value in zip(
        pulls,
        probabilities
    ):
        if probability_value >= target:
            required_pulls = pull
            break

    threshold_pulls[label] = required_pulls

# ------------------------------------------------------------
# Probability Chart
# ------------------------------------------------------------

fig = px.line(
    x=pulls,
    y=probabilities,
    labels={
        "x": "Number of Pulls",
        "y": "Chance of ≥1 SSR"
    },
    title="Chance of Getting at Least One SSR"
)

fig.update_yaxes(
    tickformat=".0%",
    range=[0, 1]
)

fig.update_layout(
    hovermode="x unified"
)

fig.update_traces(
    hovertemplate=(
        "Pulls: %{x}<br>"
        "SSR Chance: %{y:.1%}"
        "<extra></extra>"
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------------------------------------
# Probability Thresholds
# ------------------------------------------------------------

st.markdown("#### Pulls Needed to Reach Each Probability")

col1, col2, col3, col4 = st.columns(4)

columns = [col1, col2, col3, col4]

for column, (label, required_pulls) in zip(
    columns,
    threshold_pulls.items()
):

    with column:

        if required_pulls is None:
            st.metric(
                label,
                "Not reached"
            )
        else:
            st.metric(
                label,
                f"{required_pulls} pulls"
            )

if selected_game.soft_pity > 0:

    st.info(
        f"Soft pity begins after approximately "
        f"{selected_game.soft_pity} pulls in this model. "
        f"The SSR probability increases as you approach hard pity."
    )

elif selected_game.hard_pity > 0:

    st.info(
        f"This game has a hard pity at "
        f"{selected_game.hard_pity} pulls in the current model."
    )

else:

    st.info(
        "No soft or hard pity system is currently modeled "
        "for this game."
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

