from day import Day
from pt import pt
from dataclasses import dataclass


def dirpad_loc(key: str) -> pt:
    match(key):
        case '^':
            return pt(1, 0)
        case 'A':
            return pt(2, 0)

        case '<':
            return pt(0, 1)
        case 'v':
            return pt(1, 1)
        case '>':
            return pt(2, 1)
    raise RuntimeError(f'asked for wrong key {key}')


def keypad_loc(key: str) -> pt:
    match(key):
        case '7':
            return pt(0, 0)
        case '8':
            return pt(1, 0)
        case '9':
            return pt(2, 0)

        case '4':
            return pt(0, 1)
        case '5':
            return pt(1, 1)
        case '6':
            return pt(2, 1)

        case '1':
            return pt(0, 2)
        case '2':
            return pt(1, 2)
        case '3':
            return pt(2, 2)

        case '0':
            return pt(1, 3)
        case 'A':
            return pt(2, 3)
    raise RuntimeError(f'asked for wrong key {key}')

# The 'panic squares' are all on the west side, so we go west last


def seq_to(a: pt, b: pt) -> str:
    needed = b - a
    seq = []
    if needed.x > 0:
        seq += '>' * needed.x
    if needed.y > 0:
        seq += 'v' * needed.y
    if needed.y < 0:
        seq += '^' * -needed.y
    if needed.x < 0:
        seq += '<' * -needed.x
    seq += 'A'
#    print(f'seq_to {a} -> {b} : {seq}')
    return "".join(seq)


def find_padseq(code: str, loc) -> str:
    old_c = 'A'
    p = loc('A')
    seq = []
    for c in code:
        q = loc(c)
        seq += seq_to(p, q)
#        print(f'{old_c}:{c} p {p} q {q} seq {seq}')
        p = q
        old_c = c
    s = "".join(seq)
#    print(f'padseq {code} -> {s}')
    return s


def find_seq(code: str) -> str:
    seq = find_padseq(code, keypad_loc)
    seq = find_padseq(seq, dirpad_loc)
    seq = find_padseq(seq, dirpad_loc)
#    seq = find_padseq(seq, dirpad_loc)
    return seq


def num_part(code: str) -> int:
    code = code[:-1]    # Trim A
    return int(code)  # Remove leading zero


def p1(codes: list[str]) -> int:
    #    for code in codes:
    #    for code in ['379A']:
    #        seq = find_seq(code)
    #        num = num_part(code)
    #        print(f'JB {code} -> {len(seq)} * {num}: {seq}')
    #    return 0
    sequence = {code: find_seq(code) for code in codes}
    return sum([num_part(code) * len(sequence[code]) for code in codes])

# 192212 - too high


if __name__ == "__main__":
    d = Day(21)
    lines = d.read_lines()
    print(p1(lines))
