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


def find_all_ins(ins, a):
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
# - so:
#   - find missing input bits
#   - follow paths forward from missing bits
#   - swap candidates are on those paths
#   - index by missing bit, need to match up with additionals
#   - find overlap between additionals and missings
def p2(lines: list[str]) -> str:
    wires, direct_deps = parse(lines)

    def get_wires(l, prefix):
        return sorted([w for w in l if w[0] == prefix], reverse=True)

    xs = get_wires(wires, 'x')
    ys = get_wires(wires, 'y')
    in_max = len(xs)
    zs = get_wires(wires, 'z')
    zs.reverse()
    zs = zs[:in_max+1]

    all_ins = defaultdict(lambda: set())
    for w in wires:
        all_deps = find_all_ins(direct_deps, w)
        all_ins[w] = all_deps

    outs = defaultdict(lambda: set())
    for out, ins in direct_deps.items():
        for inn in ins:
            outs[inn].add(out)

    def get_paths_to(w: str) -> list[list[str]]:
        out = outs[w]
        if len(out) == 0:
            return [[w]]
        ret = []
        for o in out:
            paths = get_paths_to(o)
            for p in paths:
                ret.append([w] + p)
        return ret

    def get_paths_from(w: str) -> list[list[str]]:
        ins = direct_deps[w]
        if len(ins) == 0:
            return [[w]]
        ret = []
        for i in ins:
            paths = get_paths_from(i)
            for p in paths:
                ret.append(p + [w])
        return ret

    missing = [set() for _ in range(len(zs))]
    additional = [set() for _ in range(len(zs))]
    for i, z in enumerate(zs):
        expected = set(flatten([[f'x{j:02}', f'y{j:02}'] for j in range(i+1)]))
        got = set(get_wires(all_ins[z], 'x')) | set(get_wires(all_ins[z], 'y'))

        missing[i] = expected - got
        additional[i] = got - expected
        print(f'{z}: missing {missing} additional {additional}')

    def find_missing():
        for i, z in enumerate(zs):
            expected = set(
                flatten([[f'x{j:02}', f'y{j:02}'] for j in range(i+1)]))
            got = set(get_wires(all_ins[z], 'x')) | set(
                get_wires(all_ins[z], 'y'))

            missing = expected - got
            if len(missing) > 0:
                return sorted(list(missing))[0]
        return None

    def find_additional(xy):
        for i, z in enumerate(zs):
            expected = set(
                flatten([[f'x{j:02}', f'y{j:02}'] for j in range(i+1)]))
            got = set(get_wires(all_ins[z], 'x')) | set(
                get_wires(all_ins[z], 'y'))

            additional = got - expected
            if xy in additional:
                return z
        return None

    def find_join(p1, p2):
        for p in p1:
            if p in p2:
                return p
        return None

    def find_swap():
        xy_missing = find_missing()
        print(f'xym {xy_missing}')
        if xy_missing is None:
            return None

        z_additional = find_additional(xy_missing)
        if z_additional is None:
            raise RuntimeError(
                f'{xy_missing} missing but not additional anywhere')

        paths_from = get_paths_from(xy_missing)
        paths_to = get_paths_to(z_additional)

        for pf in paths_from:
            for pt in paths_to:
                join = find_join(pf, pt)
                if join is not None:
                    print(f'join {join} pf {pf} pt {pt}')
        return None

    find_swap()

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
