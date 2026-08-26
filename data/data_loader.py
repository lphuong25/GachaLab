import pandas as pd

from simulation import GachaGame

def load_games(file_path):
    """
    Load gacha game data from excel file
    and convert each row into an object
    """

    df = pd.read_excel(file_path)

    games = []

    for _, row in df.iterrows():
        game = GachaGame(
            name=row["Name"],
            base_rate=row["Base_rate"],
            soft_pity=row["Soft_pity"],
            soft_rate=row["Soft_rate"],
            hard_pity=row["Hard_pity"],
            cost_per_pull=row["Cost_per_pull"]
        )

        games.append(game)

    return games

# get a specific game by name
def get_game_by_name(games, name):
    for game in games:
        if game.name.lower() == name.lower():
            return game
    return None