from typing import Callable, NamedTuple, TypeVar, Sequence

matrix = list[str]


class pt(NamedTuple):
    x: int
    y: int

    def add(self, o):
        return pt(self.x+o.x, self.y+o.y)

    def __add__(self, b):
        return self.add(b)

    def sub(self, o):
        return pt(self.x-o.x, self.y-o.y)

    def __sub__(self, b):
        return self.sub(b)

    def __eq__(self, o) -> bool:
        return self.x == o.x and self.y == o.y

    def iszero(self) -> bool:
        return self == Zero

    # How to use a default value defined later in the file? :-(
    def adjacent_pts_nesw(self):
        return [p.add(self) for p in NESW]

    def manhattan_len(self) -> int:
        return abs(self.x) + abs(self.y)

    def adjacent_pts(self):
        return [p.add(self) for p in ALL_DIRS]

    def is_adjacent(self, q) -> bool:
        return q in self.adjacent_pts()

    def trim_within(self, bounds: 'pt') -> 'pt':
        x = self.x % bounds.x
        y = self.y % bounds.y
        return pt(x, y)

    def within_pt(self, bounds: 'pt') -> bool:
        ret = self.x >= 0 and self.x < bounds.x and self.y >= 0 and self.y < bounds.y
        return ret

    def within(self, m: matrix) -> bool:
        mb = matrix_bounds(m)
        return self.within_pt(mb)

    def char_at(self, m: matrix, sentinel=None) -> str:
        if not self.within(m):
            if sentinel is not None:
                return sentinel
            raise RuntimeError(f'pt {self} not within matrix')
        return m[self.y][self.x]

    def scale(self, n: int):
        return pt(self.x * n, self.y * n)

    def __repr__(self):
        return f'[{self.x},{self.y}]'

    def __str__(self):
        return self.__repr__()

    def turn_right(self):
        i = NESW.index(self)
        i += 1
        i %= 4
        return NESW[i]

    def turn_left(self):
        i = NESW.index(self)
        i -= 1
        i %= 4
        return NESW[i]

    def dist_set(self, dist, fill=False, include_self=False):
        if dist == 0:
            if include_self:
                return set(self)
            else:
                return set()
        if dist < 0:
            raise RuntimeError(f'Negative distance {dist}')
        ret = set()
        if include_self:
            ret.add(self)
        for d in range(0, dist+1):
            v1 = pt(d, dist-d)
            v2 = pt(d-dist, d)
            ret.add(self+v1)
            ret.add(self-v1)
            ret.add(self+v2)
            ret.add(self-v2)
        if fill:
            return ret.union(self.dist_set(dist-1, fill=True, include_self=include_self))
        else:
            return ret


def mk_is_adjacent(p: pt) -> Callable[[pt], bool]:
    def f(q: pt) -> bool:
        return q.is_adjacent(p)
    return f


def pt_parse(s: str) -> pt:
    # a, b - with optional whitespace
    bits = s.split(',')
    return pt(int(bits[0]), int(bits[1]))


T = TypeVar("T")


def map_find(m: Sequence[Sequence[T]], needle: T) -> list[pt]:
    found = []
    for j, l in enumerate(m):
        for i, c in enumerate(l):
            if c == needle:
                found.append(pt(i, j))
    return found


def matrix_bounds(m: matrix) -> pt:
    return pt(len(m[0]),  len(m))


Zero = pt(0, 0)


N = pt(0, -1)
E = pt(1, 0)
S = pt(0, +1)
W = pt(-1, 0)
NESW = [N, E, S, W]
NE = N.add(E)
SE = S.add(E)
NW = N.add(W)
SW = S.add(W)

ALL_DIRS = NESW + [NE, SE, SW, NW]


def dir_to_char(p: pt) -> str:
    if p == N:
        return '^'
    elif p == S:
        return 'v'
    elif p == E:
        return '>'
    elif p == W:
        return '<'
    raise RuntimeError(f'Unknown direction [{p}]')


def char_to_dir(s: str) -> pt:
    if s == '^':
        return N
    elif s == 'v':
        return S
    elif s == '>':
        return E
    elif s == '<':
        return W
    raise RuntimeError(f'Unknown direction symbol [{s}]')


# 2x2 matrix
#  a  b
#  c  d
class mat(NamedTuple):
    a: int
    b: int
    c: int
    d: int

    def times(self, p: pt) -> pt:
        return pt(self.a * p.x + self.b * p.y, self.c * p.x + self.d * p.y)

    def int_inv(self):
        return mat(self.d, -self.b, -self.c, self.a)

    def inv_det(self) -> int:
        return self.a*self.d - self.b*self.c
