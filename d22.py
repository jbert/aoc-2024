from day import Day


def next_num(a: int) -> int:
    a = ((a * 64) ^ a) % 16777216
    a = (int(a / 32) ^ a) % 16777216
    a = ((a * 2048) ^ a) % 16777216
    return a


def next_nums(l: list[int]) -> list[int]:
    return [next_num(a) for a in l]


def p1(lines: list[str]) -> int:
    nums = [int(l) for l in lines]
    print(nums)
    for _ in range(2000):
        nums = next_nums(nums)
#    print(nums)
    return sum(nums)


if __name__ == "__main__":
    d = Day(22)
    lines = d.read_lines()
    print(p1(lines))
