# GachaLab

**Is this Gacha Game actually fair?**

GachaLab in an interactive webpage that explores and demonstrate how Gacha Game mechanism and pity system work.

The application uses the public rate of obtaining an SSR, pity mechanism, and cost per pull of various Gacha Games to calculate and simulate the gacha mechanism in the featured game. It calculates the probability to obtain an SSR with a certain saved pull, current pity, and paid budget.

The project also includes Fairness Score that calculate and compare gacha system between games using expected cost, 90% cost, and worst-case cost

**Live Demo**:

-------------

**The Idea**

Gacha Games has been appeared for long time ago, but it is popularized during the COVID-19. Now, GachaGame is a big market around the globe.

I consider Gacha Game as a new form of gambling, which sparks the idea for this project. Gacha Games usually advertise their SSR rate, pity system, but as a (used to) Gacha Game players, I have always wondered the statistical mechanism behind those games. Why my luck is so high sometimes, why it is so bad the other times. To some people, it can create a kind of addiction to gambling.

Therefore, GachaLab was created to answer questions such as:

- With a certain budget, what is my probability to obtain an SSR?
- What is my probability with current saved pull?
- Does my pity affect the result?
- How many pulls are needed to reach 50%, 75%, 90% thresholds?
- How much SSR cost on average?
- Can I get a better rate with a certain budget between different games?

---------------

**Features**

**Pull Planner**

Users can enter:

- Saved pulls
- Current pity
- Spending budget

GachaLab calculates:

- Paid pulls
- Total planned pulls
- Probability of obtaining at least one SSR
- Progress toward hard pity
- Probability Analysis

The dashboard visualizes the probability of obtaining at least one SSR as the number of pulls increases.

Users can also see the number of pulls required to reach:

- 50% probability
- 75% probability
- 90% probability
- 95% probability

**GachaLab Fairness Score**

Each game receives a relative score from 0–100 based on estimated acquisition costs.

The score uses:

| Metric | Weight |
|---|---:|
| Expected Cost | 40% |
| 90% Success Cost | 40% |
| Worst-Case Cost | 20% |

Lower estimated costs result in higher scores.

**Game Comparison**

Users can compare multiple games using an interactive Fairness Score chart.

**Fairness Ranking**

The dashboard provides a ranking of all games in the dataset based on their GachaLab Fairness Score.

---

## How It Works

**1. SSR Probability** 

GachaLab calculates the probability of obtaining at least one SSR using:

- Base SSR rate
- Current pity
- Soft pity
- Soft pity rate increase
- Hard pity

For multiple pulls, the probability of obtaining at least one SSR is calculated from the probability of receiving no SSR across all planned pulls.

**2. Expected Cost**

The expected cost is estimated from the expected number of pulls required to obtain an SSR:

```text
Expected Cost =
Expected Pulls × Cost per Pull
```

**3. Probability Threshold Costs**

GachaLab determines how much spending is required to reach different probability targets.

For example:

```text
50% chance → estimated cost
75% chance → estimated cost
90% chance → estimated cost
95% chance → estimated cost
```

**4. Fairness Score**

The Fairness Score combines three cost-based measurements:

```text
40% Expected Cost
+
40% 90% Success Cost
+
20% Worst-Case Cost
```

Games with lower estimated acquisition costs receive higher relative scores.

> **Important:** The Fairness Score is relative to the games included in the current dataset and the assumptions used by GachaLab. It is not intended to represent an objective or universal definition of fairness.

---

## Simulation

GachaLab also includes Monte Carlo simulation functionality for modeling repeated gacha outcomes.

The simulation generates many independent pulling sequences and analyzes statistics such as:

- Mean pulls
- Median pulls
- Standard deviation

This provides a simulation-based perspective that complements the analytical probability calculations.

---

## Dataset

The current dataset contains gacha parameters for 20 games.

Each game includes information such as:

- Game name
- Base SSR rate
- Soft pity
- Soft pity rate
- Hard pity
- Cost per pull

The dataset is stored in:

```text
data/gachagame.xlsx
```

---

## Technology

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly**
- **OpenPyXL**
- **Pytest**

---

## Project Structure

```text
GachaLab/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── data_loader.py
│   └── gachagame.xlsx
│
├── simulation/
│   ├── analytics.py
│   ├── banner.py
│   ├── fairness.py
│   ├── gacha.py
│   ├── game.py
│   ├── probability.py
│   ├── result.py
│   ├── simulation_system.py
│   └── state.py
│
├── tests/
│   ├── test_analytics.py
│   ├── test_banner.py
│   ├── test_banner_simulation.py
│   ├── test_data_loader.py
│   ├── test_fairness.py
│   ├── test_probability.py
│   └── test_state.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Testing

The project includes automated tests covering:

- Probability calculations
- Pity mechanics
- Pull planning
- Budget calculations
- Fairness calculations
- Banner simulation
- Gacha state
- Data loading

Run the test suite with:

```bash
python -m pytest
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/lphuong25/GachaLab
cd GachaLab
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run dashboard/app.py
```

---

## Limitations

Gacha systems can contain many banner-specific mechanics. GachaLab intentionally uses a simplified model for its current analysis.

Current limitations include:

- Not contain all games on market
- Some game mechanics are simplified.
- Game-specific banner rules may differ from the model.
- Featured/rate-up SSR mechanics are not currently modeled in the dashboard.
- Pity carry-over behavior is not fully represented in the analytical dashboard.
- Costs are based on the assumptions in the dataset.
- Game mechanics and rates may change over time.
- The Fairness Score is relative to the games included in the dataset.

---

## Future Improvements

Potential future improvements include:

- Adding more game
- Featured/rate-up SSR modeling
- Banner-specific pity systems
- Pity carry-over modeling
- User-defined gacha parameters
- More frequently updated game data
- Historical comparisons of gacha systems
- Additional statistical analysis
- Expanded simulation scenarios

