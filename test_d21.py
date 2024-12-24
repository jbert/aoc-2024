from d21 import numpad, numpad_loc, seqs_to, find_seqprods


numpad_seq_test_cases = [
    ('A', '0', '<'),
    ('0', '4', ['^^<', '^<^']),
    ('A', '3', '^'),
    ('A', '2', ['^<', '<^']),
    ('A', '1', ['^<<', '<^<']),
    ('A', '4', ['<^<^', '<^^<', '^<<^', '^<^<', '^^<<']),
    ('A', '6', ['^^']),
    ('4', '9', ['>>^', '>^>', '^>>']),
]


def test_seqs_to():
    # Only one way from A to 0
    l = numpad_loc
    pad = numpad
    for tc in numpad_seq_test_cases:
        a, b, expected = tc
        print(f'tc {tc}')
#        assert len(seqs_to(l('A'), l('0'))) == 1
        expected = set([e + 'A' for e in expected])
        print(f'expected is {expected}')
        assert seqs_to(l(a), l(b), pad, l) == expected


def test_find_seqprods():
    l = numpad_loc
    code = '049'    # These all exist in numpad_seq_test_cases
    pad = numpad
    sp = find_seqprods(code, pad, l)

    print(f'sp {sp}')
    assert len(sp) == 3    # A->0, 0->4, 4->9

    def find_test_case(testcases, step):
        for tc in testcases:
            if tc[0] == step[0] and tc[1] == step[1]:
                return tc
        raise RuntimeError(f"Can't see step {step} in testcases")

    for i, step in enumerate([('A', '0'), ('0', '4'), ('4', '9')]):
        a, b, expected = find_test_case(numpad_seq_test_cases, step)
        print(f'step {step} a {a} b {b} expected {expected} sp {sp[i]}')
        assert a == step[0]
        assert b == step[1]
        assert len(expected) == len(sp[i])
        expected = set([e + 'A' for e in expected])
        assert set(sp[i]) == expected
