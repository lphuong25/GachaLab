from simulation import BannerState
from simulation.state import pulls_until_pity

def test_initial_banner_state():
    state = BannerState()

    assert state.pity == 0
    assert state.guaranteed_featured is False 

def test_guaranteed_state():
    state = BannerState(
        pity = 0,
        guaranteed_featured=True
    )  
    assert state.pity == 0
    assert state.guaranteed_featured is True

def test_pulls_until_pity():

    state = BannerState(
        pity=65
    )

    assert pulls_until_pity(
        state,
        90
    ) == 25


def test_already_at_pity():

    state = BannerState(
        pity=90
    )

    assert pulls_until_pity(
        state,
        90
    ) == 0


def test_no_hard_pity():

    state = BannerState(
        pity=50
    )

    assert pulls_until_pity(
        state,
        0
    ) is None