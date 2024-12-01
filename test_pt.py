from pt import ALL_DIRS, NESW, Zero, pt


def test_directions():
    assert len(ALL_DIRS) == 8
    assert len(set(ALL_DIRS)) == 8

    assert len(NESW) == 4
    assert len(set(NESW)) == 4

    assert pt(0, 0).iszero()

    assert set(Zero.adjacent_pts()) == set([
        pt(1, 0),
        pt(0, 1),
        pt(-1, 0),
        pt(0, -1),
        pt(1, 1),
        pt(1, -1),
        pt(-1, 1),
        pt(-1, -1),
    ])

    assert pt(3, 4).is_adjacent(pt(3, 5))
    assert pt(3, 4).is_adjacent(pt(3, 5))

    assert not pt(3, 4).is_adjacent(pt(3, 4))
