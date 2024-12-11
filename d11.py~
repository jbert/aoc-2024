from day import Day, str_to_nums, flatten

def stone_blink(n: int) -> list[int]:
    s = str(n)
    if n == 0:
        return [1]
    elif len(s) % 2 == 0:
        h = int(len(s) / 2)
        return [int(s[:h]), int(s[h:])]
    else:
        return [n * 2024]


def p1(lines: list[str]) -> int:
    stones = str_to_nums(lines[0])
    num_ticks = 25
    while num_ticks > 0:
        #        print(stones)
        stones = flatten([stone_blink(n) for n in stones])
        num_ticks -= 1
    return len(stones)


cache:dict[tuple[int,int],int] = {}
def stone_count_after(stone: int, num_ticks: int) -> int:
    v = cache.get((stone, num_ticks), None)
    if v is not None:
        return v
    if num_ticks == 0:
        return 1
    stones = stone_blink(stone)
    v = sum([stone_count_after(stone, num_ticks-1) for stone in stones])
    cache[(stone, num_ticks)] = v
    return v


def p2(lines: list[str]) -> int:
    stones = str_to_nums(lines[0])
    return sum([stone_count_after(stone, 75) for stone in stones])

if __name__ == "__main__":
    d = Day(11)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
