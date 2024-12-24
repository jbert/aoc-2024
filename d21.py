from sys import intern
from day import Day
from pt import pt, char_to_dir
from itertools import permutations, chain
from typing import Generator, Any


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


numpad = ["789", "456", "123", "X0A"]
dirpad = ["X^A", "<v>"]


def numpad_loc(key: str) -> pt:
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


def seqs_to_raw(a: pt, b: pt) -> set[str]:
    d = b - a
    dx = pt(d.x, 0)
    dy = pt(0, d.y)
    h = '>' if d.x > 0 else '<'
    v = 'v' if d.y > 0 else '^'
    nh = abs(d.x)
    nv = abs(d.y)
    # Need all perms of h and v which have nv v and nh h
    s = h * nh + v * nv
#    print(f'd {d} h {h} v {v} s {s}')
    return set(["".join(t)+'A' for t in permutations(s)])


class BadButton(RuntimeError):
    pass


def is_valid_seq_from(p, seq, pad, loc) -> bool:
    try:
        interpret_padseq_from(p, seq, pad, loc)
        return True
    except BadButton:
        return False


def seqs_to(a: pt, b: pt, pad, loc):
    seqs = seqs_to_raw(a, b)
    return set([seq for seq in seqs if is_valid_seq_from(a, seq, pad, loc)])


def find_seqprods(code: str, pad, loc) -> list[set[str]]:
    p = loc('A')
    seqprod = []
    old_c = 'A'
    for c in code:
        q = loc(c)
        if p != q:
            seqs = [seq for seq in seqs_to(p, q, pad, loc)]
            seqprod.append(seqs)
            for seq in seqs:
                s = interpret_padseq_from(p, seq, pad, loc)
                if len(s) != 1:
                    raise RuntimeError(
                        f'seq {seq} p {p} q {q} should be a single step - got [{s}]')
                if s[0] != c:
                    raise RuntimeError(
                        f'seq {seq} p {p} q {q} should be a step to {c} - got [{s}]')
#        print(f'{old_c}:{c} p {p} q {q} seq {seqprod}')
        p = q
        old_c = c
#    print(f'seqprod {code} -> {seqprod}')
    return seqprod


def expand_seqprod(seqprod: list[set[str]]) -> Generator[str, Any, None]:
    if len(seqprod) == 0:
        yield ""
        return
    for s in seqprod[0]:
        for r in expand_seqprod(seqprod[1:]):
            yield s + r


def all_codes(code, pad, loc):
    return expand_seqprod(find_seqprods(code, pad, loc))


def find_all_seqs(code: str):
    seqs = all_codes(code, numpad, numpad_loc)
    seqs = chain.from_iterable(
        [all_codes(seq, dirpad, dirpad_loc) for seq in seqs])
    seqs = chain.from_iterable(
        [all_codes(seq, dirpad, dirpad_loc) for seq in seqs])
    return seqs


def find_shortest_seq(code: str):
    minlen = 1000 * 1000 * 1000
    best = ""
    # TODO -discard those which go to an X
    num_seqs = 0
    for seq in find_all_seqs(code):
        print(f'{num_seqs} : {code} {seq}')
        num_seqs += 1
        check_code = interpret_seq(seq)
        if code != check_code:
            print(f'{num_seqs} Bad seq {seq}: check {check_code} code {code}')
            continue
        print(f'{num_seqs} Good seq {seq}: check {check_code} code {code}')
#        print(f'seq {seq} len {len(seq)}')
        ln = len(seq)
        if ln < minlen:
            minlen = ln
            best = seq
    return best


def num_part(code: str) -> int:
    code = code[:-1]    # Trim A
    return int(code)  # Remove leading zero


def interpret_seq(seq: str) -> str:
    try:
        seq = interpret_padseq(seq, dirpad, dirpad_loc)
        seq = interpret_padseq(seq, dirpad, dirpad_loc)
        seq = interpret_padseq(seq, numpad, numpad_loc)
    except BadButton:
        raise BadButton(f'seq {seq}')
    return seq


def interpret_padseq(seq, pad, loc) -> str:
    return interpret_padseq_from(loc('A'), seq, pad, loc)


def interpret_padseq_from(p, seq, pad, loc) -> str:
    #    print(f'seq {seq} p {p} pad {pad} loc {loc}')
    pushes = []
    for c in seq:
        if c == 'A':
            pushes += p.char_at(pad)
            continue
        dir = char_to_dir(c)
        p += dir
#        print(f'c {c} p {p} pad {pad} loc {loc}')
        if p.char_at(pad) == "X":
            raise BadButton(f'p {p} seq {seq} loc {loc}')
    s = "".join(pushes)
#    print(f'{code} -> {s}')
    return s


# 192212 - too high

def p1(codes: list[str]) -> int:
    #    for code in codes:
    for code in ['029A']:
        seq = find_shortest_seq(code)
        print(f"shortest seq: {seq}")
        num = num_part(code)
        print(f'JB {code} -> {len(seq)} * {num}: {seq}')
    return 0


if __name__ == "__main__":
    d = Day(21)
    lines = d.read_lines()
    print(p1(lines))
