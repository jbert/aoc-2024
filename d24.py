from day import Day, split_list
from collections.abc import Callable
from collections import defaultdict


# activated: dict[str, bool] = {}


# def clear_activated():
#    global activated
#    activated = {}


# def get_activated() -> dict[str, bool]:
#    global activated
#    return activated


def get_wire(wires: dict[str, Callable[[], bool]], wire: str) -> bool:
    v = wires[wire]()
#    activated[wire] = v
#    print(f'gw: {wire} -> {v}')
    # def get_wire(wires: dict[str, () -> bool], wire: str) -> bool:
    return v


def mk_const(b: bool):
    #    print(f'mk_const: {b}')
    return lambda:  b


def mk_xor(wires, a: str, b: str) -> Callable[[], bool]:
    def doit():
        av = get_wire(wires, a)
        bv = get_wire(wires, b)
        return av != bv
    return doit


def mk_or(wires, a: str, b: str) -> Callable[[], bool]:
    def doit():
        av = get_wire(wires, a)
        bv = get_wire(wires, b)
        return av or bv
    return doit


def mk_and(wires, a: str, b: str) -> Callable[[], bool]:
    def doit():
        av = get_wire(wires, a)
        bv = get_wire(wires, b)
        return av and bv
    return doit


def parse(lines: list[str]):
    bits = split_list(lambda l: l == "", lines)
    wires: dict[str, Callable[[], bool]] = {}
    depends_on = defaultdict(lambda: set())
    for l in bits[0]:
        wire, bval = l.split(': ')
        b = True if bval == '1' else False
        wires[wire] = mk_const(b)

    mk_funcs = {
        "XOR": mk_xor,
        "OR": mk_or,
        "AND": mk_and,
    }
    for l in bits[1]:
        lbits = l.split(' -> ')
        out = lbits[1]
        abits = lbits[0].split(' ')
        a, fname, b = abits
        depends_on[out].add(a)
        depends_on[out].add(b)
        wires[out] = mk_funcs[fname](wires, a, b)

    return wires, depends_on


def all_depends(depends_on, a):
    todo = set([a])
    ret = set()
    while len(todo) > 0:
        x = todo.pop()
        ret |= depends_on[x]
        todo |= depends_on[x]
    return ret


def bools_to_int(bs: list[bool]) -> int:
    ret = 0
    for b in bs:
        ret *= 2
        if b:
            ret += 1
    return ret


def int_to_bools_fixed(n: int, nbits: int) -> list[bool]:
    bs = int_to_bools(n)
    padlen = nbits - len(bs)
    bs = ([False] * padlen) + bs
    return bs[:nbits]


def int_to_bools(n: int) -> list[bool]:
    ret = []
    while n > 0:
        ret.append(n % 2 == 1)
        n = int(n/2)
    ret.reverse()
    return ret


def mk_overrides(x, y, xs, ys) -> dict[str, Callable[[], bool]]:
    nbits = len(xs)
    xvs = int_to_bools_fixed(x, nbits)
    yvs = int_to_bools_fixed(y, nbits)
    overrides = {xs[i]: mk_const(xvs[i]) for i in range(nbits)}
    overrides.update({ys[i]: mk_const(yvs[i]) for i in range(nbits)})
    return overrides


def is_adder(wires, xs, ys) -> bool:
    x = 1
    y = 1
    xyoverrides = mk_overrides(x, y, xs, ys)
    # print(xyoverrides)
    z = eval_with_swaps(wires, overrides=xyoverrides)
    # print(z)
    return z == x + y


# ok, in terms of dependencies between x, y and z
# z00 must depend exactly on x00, y00
# z01 must depend exactly on x00, y00, x01, y01
# etc
#
# we have only 4 swaps
# So:
# - loop over z bits, starting with low bits
# - find first 'additional' or 'missing' input bits
# - swap candidates are wires with dependencies on those input bits (including inputs and outputs?)
# - intersection of all candidates gives answer?
def p2(lines: list[str]) -> str:
    wires, depends_on = parse(lines)
    xs = sorted([w for w in wires.keys() if w[0] == 'x'], reverse=True)
    ys = sorted([w for w in wires.keys() if w[0] == 'y'], reverse=True)
    zwires = sorted([w for w in wires.keys() if w[0] == 'z'], reverse=True)

#    print(f'num_wires {len(wires)}')
    print(all_depends(depends_on, 'z44'))

    if is_adder(wires, xs, ys):
        print('yay')
    lswaps = ['not', 'found']
    return "".join(sorted(lswaps))


def do_swaps(wires, swaps):
    for f, t in swaps:
        wires[f], wires[t] = wires[t], wires[f]


def eval_with_swaps(wires, swaps=[], overrides={}) -> int:
    zwires = sorted([w for w in wires.keys() if w[0] == 'z'], reverse=True)
#    print(wires)
#    print(zwires)
#    for zw in zwires:
#        print(f'zw {zw}: {wires[zw]()}')
    for wire, val in overrides.items():
        #        print(f'overriding wire {wire} {val()}')
        wires[wire] = val
#    do_swaps(wires, swaps)
    bs = [wires[zw]() for zw in zwires]
#    do_swaps(wires, swaps)
    return bools_to_int(bs)


def p1(lines: list[str]) -> int:
    wires, _ = parse(lines)
    return eval_with_swaps(wires)


if __name__ == "__main__":
    d = Day(24)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
