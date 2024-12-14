from day import Day
from pt import pt, pt_parse, N
from dataclasses import dataclass
import math


@dataclass
class robot:
    pos: pt
    vel: pt
    arena: pt

    def trim(self):
        self.pos = self.pos.trim_within(self.arena)

    def tick(self):
        self.pos += self.vel
        self.trim()

    def warp(self, num_ticks: int):
        self.pos += self.vel.scale(num_ticks)
        self.trim()

    def within(self, bounds: pt) -> bool:
        return self.pos.within_pt(bounds)


def parse_line(s: str) -> robot:
    bits = s.split(' ')
    p = pt_parse(bits[0][2:])
    v = pt_parse(bits[1][2:])
    return robot(p, v, pt(0, 0))


def parse(lines: list[str]) -> list[robot]:
    return [parse_line(l) for l in lines]


def print_robots(arena: pt, robots: list[robot]):
    for j in range(arena.y):
        line = ""
        for i in range(arena.x):
            count = 0
            p = pt(i, j)
            for r in robots:
                if r.pos == p:
                    count += 1
            line += str(count)
        print(line)


def is_symmetric(ps: set[pt], x: int) -> bool:
    while len(ps) > 0:
        p = ps.pop()
        qx = x - p.x
        q = pt(qx, p.y)
        if q not in ps:
            return False
        ps.remove(q)
    return True


def stack_size(p: pt, ps: set[pt]) -> int:
    stack = 0
    while p in ps:
        p = p.add(N)
        stack += 1
    return stack


def vertical_stack(ps: set[pt]) -> int:
    return max([stack_size(p, ps) for p in ps])


def possible_tree(ps: set[pt]) -> bool:
    return vertical_stack(ps) > 10


def p2(lines: list[str], arena: pt) -> int:
    robots = parse(lines)
    for r in robots:
        r.arena = arena
    x2 = int(arena.x / 2)
    max_tick = 101*103
    for tick in range(1, max_tick+10):
        for r in robots:
            r.tick()
        posses = set([r.pos for r in robots])
#        if len(posses.intersection(tree)) == len(tree) or tick % 1000 == 0:
        should_print = possible_tree(posses)
        if should_print:
            if should_print:
                print(f'MSG: {tick} Found!?')
            print_robots(arena, robots)
            print("")
            return tick


def find_ticks(r: robot, x: int) -> list[int]:
    x2 = int(x / 2)
    count = 0
    while r.pos.x != x2:
        r.tick()
        count += 1
    first = count

    r.tick()
    count += 1
    while r.pos.x != x2:
        r.tick()
        count += 1
    second = count

    r.tick()
    count += 1
    while r.pos.x != x2:
        r.tick()
        count += 1
    return [first, second, count]


# OK - this wasn't the solution, but it did remind me that every point will return
# to it's starting pos in 101*103 ticks, so the problem wasn't a slow simulation,
# the problem was better recognition
def p2_nope(lines: list[str], arena: pt) -> int:
    robots = parse(lines)
    for r in robots:
        r.arena = arena
    # The tree must by symmetric about the vertical axis and must have
    # several robots on the vertical axis
    # So let's find ticks in the future when a given robot will be on the vertical
    # axis and then print those
    # We are in an additive p-group (103 and 101 are both prime)
    # So each x-coord will cycle every 103 and each y-coord every 101
    poss_ticks = [find_ticks(r, arena.x) for r in robots]
    print(poss_ticks)
    return 0


def p1(lines: list[str], arena: pt) -> int:
    robots = parse(lines)
    for r in robots:
        r.arena = arena
    for _ in range(0, 100):
        for r in robots:
            r.tick()

    x2 = int(arena.x / 2)
    y2 = int(arena.y / 2)
    quads = [0, 0, 0, 0]
    for r in robots:
        if r.pos.x < x2 and r.pos.y < y2:
            quads[0] += 1
        elif r.pos.x > x2 and r.pos.y < y2:
            quads[1] += 1
        elif r.pos.x < x2 and r.pos.y > y2:
            quads[2] += 1
        elif r.pos.x > x2 and r.pos.y > y2:
            quads[3] += 1

#    print(quads)
    return math.prod(quads)


if __name__ == "__main__":
    d = Day(14)
    lines = d.read_lines()
    arena = pt(101, 103)
    if d.suffix != "":
        arena = pt(11, 7)
    print(p1(lines, arena))
    print(p2(lines, arena))
