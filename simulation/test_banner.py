from simulation import Banner

def test_banner():
    banner = Banner(
        name="Character Event Banner",
        featured_rate=0.5,
        guarantee_rate=0.5,
        pity_carries=True,
        guarantee_carries=True
    )

    assert banner.name == "Character Event Banner"
    assert banner.featured_rate == 0.5
    assert banner.guarantee_rate == 0.5
    assert banner.pity_carries is True
    assert banner.guarantee_carries is True    