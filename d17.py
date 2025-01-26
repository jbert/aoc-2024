from day import Day, split_list, str_to_nums, flatten
from dataclasses import dataclass
from typing import NamedTuple, Optional


@dataclass
class machine:
    A: int
    B: int
    C: int
    ip: int

    output: list[int]

    def out(self, n):
        self.output.append(n)

    def execute(self, ops) -> list[int]:
        while True:
            if self.ip >= len(ops):
                break
            op = ops[self.ip]
            op.exec(self)
            self.ip += 1
        return self.output

    def print(self, op):
        print(f'ip {self.ip} A {self.A} B {self.B} C {self.C}: {op}')


class op(NamedTuple):
    instruction: int
    operand: int

    def __str__(self):
        return f'[{self.instruction}, {self.operand}]'

    def __repr__(self):
        return f'{self}'

    def exec(self, m: machine):
        match(self[0]):
            case 0:
                # The adv instruction (opcode 0) performs division. The
                # numerator is the value in the A register. The denominator is
                # found by raising 2 to the power of the instruction's combo
                # operand.
                # The result of the division operation is truncated to an
                # integer and then written to the A register.
                m.A = int(m.A / (2 ** self.combo(m)))
            case 1:
                # The bxl instruction (opcode 1) calculates the bitwise XOR of
                # register B and the instruction's literal operand, then stores
                # the result in register B.
                m.B = m.B ^ self.operand
            case 2:
                # The bst instruction (opcode 2) calculates the value of its
                # combo operand modulo 8 (thereby keeping only its lowest 3
                # bits), then writes that value to the B register.
                m.B = self.combo(m) % 8
            case 3:
                # The jnz instruction (opcode 3) does nothing if the A register
                # is 0. However, if the A register is not zero, it jumps by
                # setting the instruction pointer to the value of its literal
                # operand; if this instruction jumps, the instruction pointer
                # is not increased by 2 after this instruction.
                if m.A != 0:
                    m.ip = self.operand - 1
            case 4:
                # The bxc instruction (opcode 4) calculates the bitwise XOR of
                # register B and register C, then stores the result in register
                # B. (For legacy reasons, this instruction reads an operand but
                # ignores it.)
                m.B = m.B ^ m.C
            case 5:
                # The out instruction (opcode 5) calculates the value of its
                # combo operand modulo 8, then outputs that value. (If a
                # program outputs multiple values, they are separated by
                # commas.)
                m.out(self.combo(m) % 8)
            case 6:
                # The bdv instruction (opcode 6) works exactly like the adv
                # instruction except that the result is stored in the B
                # register. (The numerator is still read from the A register.)
                m.B = int(m.A / (2 ** self.combo(m)))
            case 7:
                # The cdv instruction (opcode 7) works exactly like the adv
                # instruction except that the result is stored in the C
                # register. (The numerator is still read from the A register.)
                m.C = int(m.A / (2 ** self.combo(m)))
            case _:
                raise RuntimeError(f'Invalid instruction {self[0]}')

    def combo(self, m) -> int:
        if self.operand >= 0 and self.operand <= 3:
            return self.operand
        if self.operand == 4:
            return m.A
        if self.operand == 5:
            return m.B
        if self.operand == 6:
            return m.C
        raise RuntimeError(f'Invalid combo {self.operand}')


def parse_register(s: str) -> int:
    colon = s.index(':')
    return int(s[colon+1:])


def parse_ops(s: str) -> list[op]:
    ops = []
    colon = s.index(':')
    nums = str_to_nums(s[colon+1:], ',')
    if len(nums) % 2 != 0:
        raise RuntimeError(f"Can't parse ops {len(s)}")
    for i in range(int(len(nums)/2)):
        ops.append(op(nums[2*i], nums[2*i+1]))
    return ops


def parse(lines: list[str]) -> tuple[machine, list[op]]:
    bits = split_list(lambda l: l == "", lines)
    if len(bits[0]) != 3:
        raise RuntimeError(f'invalid number of registers {len(bits[0])}')
    if len(bits[1]) != 1:
        raise RuntimeError(f'invalid operand list {len(bits[1])}')
    a = parse_register(bits[0][0])
    b = parse_register(bits[0][1])
    c = parse_register(bits[0][2])
    ops = parse_ops(bits[1][0])
    m = machine(a, b, c, 0, [])
    return m, ops


# Program:
# Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
# 2,4 1,5 7,5 1,6 0,3 4,2 5,5 3,0
#
# A = Sum(ak * 8^k), k=0,n
#
# bst A     ; B = A % 8
# B = a0
# bxl 5     ; B = B XOR 5 (101)
# B = a0 XOR 5
# cdv B     ; C = A >> B
# C = high bits of A shifted down 0-7
# bxl 6     ; B = B XOR 6 (110)
# B = a0 XOR 3
# adv 3     ; A /= 8
# A = Sum(a(k+1) * 8^k), k=0,n-1
# bxc       ; B = B XOR C
# B = a0 XOR 3 XOR high bits of A shifted down 0-7
# out B     ; out B % 8
# jnz 0

# Shifting down 0-7 bits means we need only vary 3 octal digits to guess each digit


# ops are:
# - A = A shift right 0-7 bits
# - B = A shift right 0-7 bits
# - C = A shift right 0-7 bits
# - B = B XOR 0..7
# - B = B XOR C
# - B = x mod 8

trio = tuple[int, int, int]


def all_trios():
    for a in range(1, 10):
        for b in range(1, 10):
            for c in range(1, 10):
                yield (a, b, c)


def find_options(digit, w, wanted, lines) -> set[trio]:

    def matches(trio) -> bool:
        m, ops = parse(lines)
        a = [1] * len(wanted)
        a[digit-2] = trio[0]
        a[digit-1] = trio[1]
        a[digit-0] = trio[2]
#        print(f'a {a}')
        m.A = int("".join([str(dig) for dig in a]))
#        print(f'm.A {m.A}')
        out = m.execute(ops)
#        print(f'out {out}')
#        print(f'wan {wanted}')
#        print(f'digit {digit} w {w}')
        return out[digit] == w

    return set(filter(matches, all_trios()))


def options_match(a: trio, b: trio) -> bool:
    return a[1] == b[0] and a[2] == b[1]


def filter_option_pair(aos: set[trio], bos: set[trio]) -> tuple[set[trio], set[trio]]:
    if len(aos) == 0 or len(bos) == 0:
        raise RuntimeError(f'zero input')
    reta = set()
    retb = set()
    for ao in aos:
        for bo in bos:
            if options_match(ao, bo):
                reta.add(ao)
                retb.add(bo)
    return reta, retb


def collapse_options(all_options: list[set[trio]]) -> list[trio]:
    print(f'all_options {all_options}')
    for i, bos in enumerate(all_options):
        if i == 0:
            continue
        aos = all_options[i-1]
        print(f'i {i} before AOS {aos} BOS {bos}')
        aos, bos = filter_option_pair(aos, bos)
        print(f'i {i} after AOS {aos} BOS {bos}')
        all_options[i-1] = aos
        all_options[i] = bos
    ret = []
    for i, bos in enumerate(all_options):
        if len(bos) != 1:
            raise RuntimeError(f'i {i} bos {bos} - not just one option')
        bo = bos.pop()
        ret.append(bo)

    return ret


def p2(lines: list[str]) -> list[int]:
    _, ops = parse(lines)
    wanted = flatten(ops)

    print(f'len(wanted) {len(wanted)} wanted {wanted}')
    all_options: list[set[trio]] = []
    for digit, w in enumerate(wanted):
        # We can examine all 3-digit octal sequences to find the ones which give us the digit in this position
        # For each position, we can find a set of (i,j,k) tuples which give us the digit
        # We can then start at one end and intersect the two overlapping digits to reduce options
        print(f'digit {digit} w {w}')
        all_options.append(find_options(digit, w, wanted, lines))
    print('========= got options ============')
    ret = collapse_options(all_options)
    print(ret)
    return ret


def p1(lines: list[str]) -> list[int]:
    m, ops = parse(lines)
    return m.execute(ops)


if __name__ == "__main__":
    d = Day(17)
    lines = d.read_lines()
    l = p1(lines)
    print(",".join([str(n) for n in l]))
    l = p2(lines)
    print(",".join([str(n) for n in l]))
