from day import Day, split_list, str_to_nums, flatten
from dataclasses import dataclass
from typing import NamedTuple
from copy import deepcopy


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


def eval(m_orig: machine, ops: list[op], a: int, pad_to: int):
    m = deepcopy(m_orig)
    m.A = a
    out = m.execute(ops)
    pad = pad_to - len(out)
    return [0] * pad + out


def p2(lines: list[str]) -> list[int]:
    m, ops = parse(lines)
    wanted = flatten([[op.instruction, op.operand] for op in ops])

    l = len(wanted)
#    digit = l - 3
    digit = 4
    for os in range(8*8*8*8*8):   # 3 octal digits worth of range
        a = pow(8, l)
        a += 1 * pow(8, 0)
        a += 1 * pow(8, 1)
        a += 4 * pow(8, 2)
        a += 7 * pow(8, 3)
        a += 3 * pow(8, 4)
        a += os * pow(8, digit)
        got = eval(m, ops, a, l)
        s = oct(a)[2:]
        print(f'{s:0>16} {got}')
        print(f'len(got) {len(got)}')

    print(f'len(wanted) {len(wanted)} wanted {wanted}')
    return []


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
