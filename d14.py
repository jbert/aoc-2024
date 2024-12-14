from day import Day
from pt import pt, pt_parse
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

    def within(self, bounds: pt) -> bool:
        return self.pos.within_pt(bounds)


def parse_line(s: str) -> robot:
    bits = s.split(' ')
    p = pt_parse(bits[0][2:])
    v = pt_parse(bits[1][2:])
    return robot(p, v, pt(0, 0))


def parse(lines: list[str]) -> list[robot]:
    return [parse_line(l) for l in lines]


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

    print(quads)
    return math.prod(quads)


if __name__ == "__main__":
    d = Day(14)
    lines = d.read_lines()
    arena = pt(101, 103)
    if d.suffix != "":
        arena = pt(11, 7)
    print(p1(lines, arena))
