from day import Day, split_list, flatten
from collections.abc import Callable
from collections import defaultdict


def get_wire(wires: dict[str, Callable[[], bool]], wire: str) -> bool:
    v = wires[wire]()
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
    ins = defaultdict(lambda: set())
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
        ins[out].add(a)
        ins[out].add(b)
        wires[out] = mk_funcs[fname](wires, a, b)

    return wires, ins


def all_ins(ins, a):
    todo = set([a])
    ret = set()
    while len(todo) > 0:
        x = todo.pop()
        ret |= ins[x]
        todo |= ins[x]
    return ret


def bools_to_int(bs: list[bool]) -> int:
    ret = 0
    for b in bs:
        ret *= 2
        if b:
            ret += 1
    return ret


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
    wires, direct_deps = parse(lines)

    def get_wires(l, prefix):
        return sorted([w for w in l if w[0] == prefix], reverse=True)

    xs = get_wires(wires, 'x')
    ys = get_wires(wires, 'y')
    zs = get_wires(wires, 'z')
    zs.reverse()
    in_max = len(xs)

    ins = defaultdict(lambda: set())
    outs = defaultdict(lambda: set())
    for w in wires:
        all_deps = all_ins(direct_deps, w)
        ins[w] = all_deps
        for d in all_deps:
            outs[d].add(w)

    poss_left = {}
    poss_right = {}
    all_missing = set()
    for i, z in enumerate(zs):
        upto = min(i, in_max)
        expected = set(flatten([[f'x{j:02}', f'y{j:02}'] for j in range(upto+1)]))
        got = set(get_wires(ins[z], 'x')) | set(get_wires(ins[z], 'y'))
#        print(i, z, upto)
#        print(expected)
#        print(got)
        missing = expected - got
#        print(missing)
        all_missing |= missing
        poss_left[i] = set(flatten([outs[mi] for mi in missing]))
        poss_right[i] = (ins[z] - set(xs)) - set(ys)

    print(all_missing)
    for i,(k,v) in enumerate(poss_left.items()):
        print(k)
        print(sorted(v))
        print(sorted(poss_right[i]))

    return ""


def eval_wires(wires, swaps=[], overrides={}) -> int:
    zwires = sorted([w for w in wires.keys() if w[0] == 'z'], reverse=True)
    bs = [wires[zw]() for zw in zwires]
    return bools_to_int(bs)


def p1(lines: list[str]) -> int:
    wires, _ = parse(lines)
    return eval_wires(wires)


if __name__ == "__main__":
    d = Day(24)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
