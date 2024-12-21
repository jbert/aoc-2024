from day import Day
from pt import pt, char_to_dir
from itertools import permutations


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


def seqs_to(a: pt, b: pt) -> set[str]:
    d = b - a
    h = '>' if d.x > 0 else '<'
    v = 'v' if d.y > 0 else '^'
    nv = abs(d.x)
    nh = abs(d.y)
    # Need all perms of h and v which have nv v and nh h
    s = h * nh + v * nv
    return set(["".join(t) for t in permutations(s)])


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


def find_padseqs(code: str, loc) -> list[set[str]]:
    p = loc('A')
    padseq = []
    for c in code:
        q = loc(c)
        padseq.append(seqs_to(p, q))
    #        print(f'{old_c}:{c} p {p} q {q} seq {seq}')
        p = q
    #    print(f'padseq {code} -> {s}')
    return padseq


def find_padseq(code: str, loc) -> str:
    p = loc('A')
    seq = []
    for c in code:
        q = loc(c)
        seq += seq_to(p, q)
    #        print(f'{old_c}:{c} p {p} q {q} seq {seq}')
        p = q
    s = "".join(seq)
    #    print(f'padseq {code} -> {s}')
    return s


def all_codes(seq: list[set[str]]):


def find_seqs(code: str) -> list[set[str]]:
    seq = find_padseqs(code, numpad_loc)
    seq = [find_padseq(seq, dirpad_loc) for code in all_codes(seq)]
    seq = [find_padseq(seq, dirpad_loc) for code in all_codes(seq)]
    return seq


def find_seq(code: str) -> str:
    seq = find_padseq(code, numpad_loc)
    seq = find_padseq(seq, dirpad_loc)
    seq = find_padseq(seq, dirpad_loc)
    #    seq = find_padseq(seq, dirpad_loc)
    return seq


def num_part(code: str) -> int:
    code = code[:-1]    # Trim A
    return int(code)  # Remove leading zero


def interpret_seq(code: str) -> str:
    seq = interpret_padseq(code, dirpad, dirpad_loc)
    seq = interpret_padseq(seq, dirpad, dirpad_loc)
    seq = interpret_padseq(seq, numpad, numpad_loc)
    return seq


def interpret_padseq(code, pad, loc) -> str:
    p = loc('A')
    pushes = []
    for c in code:
        if c == 'A':
            pushes += p.char_at(pad)
            continue
        dir = char_to_dir(c)
        p += dir
    s = "".join(pushes)
    print(f'{code} -> {s}')
    return s


def p1(codes: list[str]) -> int:
    for code in codes:
        seq = find_seq(code)
        check = interpret_seq(seq)
        if check != code:
            raise RuntimeError(
                f"Something's wrong: got {check} expected {code}")
        num = num_part(code)
        print(f'JB {code} -> {len(seq)} * {num}: {seq}')
    return 0
    #    sequence = {code: find_seq(code) for code in codes}
    #    return sum([num_part(code) * len(sequence[code]) for code in codes])

    # 192212 - too high


if __name__ == "__main__":
    d = Day(21)
    lines = d.read_lines()
    print(p1(lines))
