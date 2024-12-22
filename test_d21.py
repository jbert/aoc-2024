from pt import pt
from d21 import numpad, numpad_loc, seqs_to


def test_seqs_to():
    # Only one way from A to 0
    test_cases = [
        ('A', '0', '<'),
        ('A', '3', '^'),
        ('A', '2', ['^<', '<^']),
        ('A', '1', ['^<<', '<^<']),
        ('A', '4', ['<^<^', '<^^<', '^<<^', '^<^<', '^^<<']),
        ('A', '6', ['^^']),
        ('4', '9', ['>>^', '>^>', '^>>']),
    ]
    l = numpad_loc
    pad = numpad
    for tc in test_cases:
        a, b, expected = tc
        print(f'tc {tc}')
#        assert len(seqs_to(l('A'), l('0'))) == 1
        expected = set([e + 'A' for e in expected])
        print(f'expected is {expected}')
        assert seqs_to(l(a), l(b), pad, l) == expected
