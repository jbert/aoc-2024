from day import Day, str_to_nums
from itertools import zip_longest


def ops(n) -> list[list[str]]:
    if n <= 0:
        return [[]]
    ll = ops(n-1)
    return [l[:] + ['+'] for l in ll] + [l[:] + ['*'] for l in ll]


def parse(lines) -> list[tuple[int, list[int]]]:
    def parse_one(l):
        colon = l.index(':')
        return int(l[:colon]), str_to_nums(l[colon+1:])

    return [parse_one(l) for l in lines]


def eval(nums: list[int], ops: list[str]) -> int:
    total = nums[0]
    for n, op in zip_longest(nums[1:], ops):
        if op == '+':
            total += n
        elif op == '*':
            total *= n
        else:
            raise RuntimeError(f'bad op {op}')
    return total


def is_true(eq) -> bool:
    total, nums = eq
    return total in [eval(nums, op) for op in ops(len(nums)-1)]


def p1(lines: list[str]) -> int:
    eqs = parse(lines)
#    print(eqs)
#    print(list(ops(3)))
    true_eqs = list(filter(is_true, eqs))
#    print(true_eqs)

    return sum([eq[0] for eq in true_eqs])


if __name__ == "__main__":
    d = Day(7)
    lines = d.read_lines()
    print(p1(lines))
