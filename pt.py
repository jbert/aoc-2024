from typing import NamedTuple, Callable

matrix = list[str]


class pt(NamedTuple):
    x: int
    y: int

    def add(self, o):
        return pt(self.x+o.x, self.y+o.y)

    def sub(self, o):
        return pt(self.x-o.x, self.y-o.y)

    def __eq__(self, o) -> bool:
        return self.x == o.x and self.y == o.y

    def iszero(self) -> bool:
        return self == Zero

    def adjacent_pts(self):
        return [p.add(self) for p in ALL_DIRS]

    def is_adjacent(self, q) -> bool:
        return q in self.adjacent_pts()

    def within(self, m: matrix) -> bool:
        mb = matrix_bounds(m)
        ret = self.x >= 0 and self.x < mb.x and self.y >= 0 and self.y < mb.y
#        print(f'within {self} - {mb} - ret {ret}')
        return ret

    def char_at(self, m: matrix) -> str:
        if not self.within(m):
            raise RuntimeError(f'pt {self} not within matrix')
        return m[self.y][self.x]

    def scale(self, n: int):
        return pt(self.x * n, self.y * n)


def mk_is_adjacent(p: pt) -> Callable[[pt], bool]:
    def f(q: pt) -> bool:
        return q.is_adjacent(p)
    return f


def matrix_bounds(m: matrix) -> pt:
    return pt(len(m[0]),  len(m))


Zero = pt(0, 0)

NESW = [
    pt(0, 1),
    pt(1, 0),
    pt(0, -1),
    pt(-1, 0),
]

ALL_DIRS = NESW + [
    pt(1, 1),
    pt(-1, 1),
    pt(1, -1),
    pt(-1, -1),
]
