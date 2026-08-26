from data_loader import load_games, get_game_by_name


def test_load_games():

    games = load_games("data/gachagame.xlsx")

    assert len(games) > 0


def test_game_names():

    games = load_games("data/gachagame.xlsx")

    names = [game.name for game in games]

    assert "Genshin Impact" in names


def test_find_game():

    games = load_games("data/gachagame.xlsx")

    game = get_game_by_name(
        games,
        "Genshin Impact"
    )

    assert game is not None
    assert game.name == "Genshin Impact"