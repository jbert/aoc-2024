from day import range_subtract


def test_range_subtract():
    test_cases = [
        [
            range(2, 5),
            range(7, 10),
            None,
            [range(2, 5)],
        ],
        [
            range(7, 10),
            range(2, 5),
            None,
            [range(7, 10)],
        ],
        [
            range(2, 7),
            range(5, 10),
            range(5, 7),
            [range(2, 5)],
        ],
        [
            range(2, 7),
            range(7, 10),
            None,
            [range(2, 7)],
        ],
        [
            range(7, 10),
            range(2, 7),
            None,
            [range(7, 10)],
        ],
        [
            range(2, 10),
            range(5, 7),
            range(5, 7),
            [range(2, 5), range(7, 10)],
        ],
        [
            range(2, 10),
            range(2, 7),
            range(2, 7),
            [range(7, 10)],
        ],
    ]

    for tc in test_cases:
        a, b, expected_ri, expected_rest = tc
        got_ri, got_rest = range_subtract(a, b)
        assert got_ri == expected_ri
        assert got_rest == expected_rest
