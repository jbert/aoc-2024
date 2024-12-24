from day import Day, split_list
from typing import Callable, NamedTuple


def get_wire(wires: dict[str, Callable[[], bool]], wire: str) -> bool:
    # def get_wire(wires: dict[str, () -> bool], wire: str) -> bool:
    return wires[wire]()


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
        wires[out] = mk_funcs[fname](wires, a, b)

    return wires


def bools_to_int(bs: list[bool]) -> int:
    ret = 0
    for b in bs:
        ret *= 2
        if b:
            ret += 1
    return ret


def p1(lines: list[str]) -> int:
    wires = parse(lines)
    zwires = sorted([w for w in wires.keys() if w[0] == 'z'], reverse=True)
#    print(wires)
#    print(zwires)
#    for zw in zwires:
#        print(f'zw {zw}: {wires[zw]()}')
    bs = [wires[zw]() for zw in zwires]
    return bools_to_int(bs)


if __name__ == "__main__":
    d = Day(24)
    lines = d.read_lines()
    print(p1(lines))
