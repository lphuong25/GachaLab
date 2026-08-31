from simulation import BannerState

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