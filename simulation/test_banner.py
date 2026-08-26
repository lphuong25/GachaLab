from simulation import Banner
from simulation.banner import featured_probability

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

def test_featured_probability():

    banner = Banner(
        name="Character Event Banner",
        featured_rate=0.5
    )

    assert featured_probability(banner) == 0.5


def test_guaranteed_featured_probability():

    banner = Banner(
        name="Character Event Banner",
        featured_rate=0.5
    )

    assert featured_probability(
        banner,
        guaranteed_featured=True
    ) == 1.0