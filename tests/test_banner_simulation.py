from simulation import (
    GachaGame,
    Banner,
    BannerState
)
from simulation.banner import pull

def test_no_ssr_increased_pity():
    game = GachaGame(
        name="Test Game",
        base_rate=0.0
    )

    banner = Banner(
        name="Test Banner",
        featured_rate=0.5
    )

    state = BannerState()

    result = pull(
        game, 
        banner,
        state,
        pull_number=1
    )

    assert result.is_ssr is False
    assert state.pity == 1

def test_hard_pity_produces_ssr():
    game = GachaGame(
        name="Test Game",
        base_rate=0.0,
        hard_pity=1
    )

    banner = Banner(
        name="Test Banner",
        featured_rate=1.0
    )

    state = BannerState()

    result = pull(
        game,
        banner,
        state,
        pull_number=1
    )

    assert result.is_ssr is True
    assert result.is_featured is True
    assert state.pity == 0

def test_guaranteed_feature():
    game = GachaGame(
        name="Test Game",
        base_rate=1.0,
    )

    banner = Banner(
        name="Test Banner",
        featured_rate=0.0
    )

    state = BannerState(
        guaranteed_featured=True
    )

    result = pull(
        game,
        banner,
        state,
        pull_number=1
    )

    assert result.is_ssr is True
    assert result.is_featured is True
    assert state.guaranteed_featured is False