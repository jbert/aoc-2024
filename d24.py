from day import Day, split_list, flatten
from collections.abc import Callable
from collections import defaultdict


def get_wire(wires: dict[str, Callable[[], bool]], wire: str) -> bool:
    print(f'gw {wire}')
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

#    with open('d24.dot', 'w') as f:
#        f.write('strict digraph {\n')
#        for w in wires:
#            for i in ins[w]:
#                f.write(f'{i} -> {w}\n')
#        f.write('}\n')

    return wires, ins


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
    for i in range(len(xs)):
        x = 1 << i
        y = 1 << i

#        print(f'is_adder i {i}/{len(xs)} x {x} y {y}')
        xyoverrides = mk_overrides(x, y, xs, ys)
        # print(xyoverrides)
        z = eval_wires(wires, overrides=xyoverrides)
        # print(z)
        print(f'x {x} y {y} z {z}')
        if z != x + y:
            return False
    return True


def bools_to_int(bs: list[bool]) -> int:
    ret = 0
    for b in bs:
        ret *= 2
        if b:
            ret += 1
    return ret


def get_wires(l, prefix):
    return sorted([w for w in l if w[0] == prefix], reverse=True)


def find_all_ins(ins, a):
    todo = set([a])
    ret = set()
    while len(todo) > 0:
        x = todo.pop()
        ret |= ins[x]
        todo |= ins[x]
    return ret


def p2(lines: list[str]) -> str:
    wires, direct_deps = parse(lines)

    xs = get_wires(wires, 'x')
    in_max = len(xs)
    ys = get_wires(wires, 'y')
    zs = get_wires(wires, 'z')

    all_ins = defaultdict(lambda: set())
    for w in wires:
        all_deps = find_all_ins(direct_deps, w)
        all_ins[w] = all_deps

    outs = defaultdict(lambda: set())
    for out, ins in direct_deps.items():
        for inn in ins:
            outs[inn].add(out)

    def get_paths_from(w: str) -> list[list[str]]:
        out = outs[w]
        if len(out) == 0:
            return [[w]]
        ret = []
        for o in out:
            paths = get_paths_from(o)
            for p in paths:
                ret.append([w] + p)
        return ret

    missing = set()
    for i, z in enumerate(zs[:in_max]):
        expected = set(flatten([[f'x{j:02}', f'y{j:02}'] for j in range(i+1)]))
        got = set(get_wires(all_ins[z], 'x')) | set(get_wires(all_ins[z], 'y'))

        missing |= expected - got
#        print(f'{z}: missing {missing}')

    print(f'missing {missing}')
    pf = set(flatten(flatten([get_paths_from(xy) for xy in missing])))
    print(f'paths_from(missing) {pf}')
    swappable_a = pf - set(xs) - set(ys) - set(zs)
    print(f'swappable_a {swappable_a}')
    swappable_b = set(wires.keys()) - set(xs) - set(ys) - swappable_a
    print(f'swappable_b {swappable_b}')

    def find_pairs(aset: set[str], bset: set[str]):
        todo = aset.copy()
        while len(todo) > 0:
            a = todo.pop()
            for b in bset - all_ins[a]:
                if a != b and a not in all_ins[b]:
                    yield (a, b)

    count = 0

    def subtract_ins(ps, t):
        return ps - set(t) - set(all_ins[t[0]]) - set(all_ins[t[1]])

    for p1 in find_pairs(swappable_a, swappable_b):
        print('p1 {p1}')
        pool2 = subtract_ins(swappable_a, p1)
        for p2 in find_pairs(pool2, swappable_b):
            print('p2 {p2}')
            pool3 = subtract_ins(pool2, p2)
            for p3 in find_pairs(pool3, swappable_b):
                print('p3 {p3}')
                pool4 = subtract_ins(pool3, p3)
                for p4 in find_pairs(pool4, swappable_b):
                    print('p4 {p4}')
                    swaps = [p1, p2, p3, p4]
#                    if count % 10_000 == 0:
                    print(
                        f'JB {count}: {swaps} {len(swappable_a)} {len(swappable_b)} {len(pool2)} {len(pool3)} {len(pool4)} ')
                    do_swaps(wires, swaps)
                    if is_adder(wires, xs, ys):
                        print(f'found it!')
                        return ",".join(sorted(flatten([list(t) for t in swaps])))
                    do_swaps(wires, swaps)
                    count += 1

    return "not found"


def do_swaps(wires, swaps: list[tuple[str, str]]):
    for f, t in swaps:
        wires[f], wires[t] = wires[t], wires[f]


def eval_wires(wires, overrides={}) -> int:
    zwires = sorted([w for w in wires.keys() if w[0] == 'z'], reverse=True)

    for wire, val in overrides.items():
        #        print(f'overriding wire {wire} {val()}')
        wires[wire] = val
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
