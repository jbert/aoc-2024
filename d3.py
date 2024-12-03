from day import Day, flatten
from typing import NamedTuple
import re


class Mul(NamedTuple):
    left: int
    right: int

    def prod(self) -> int:
        return self.left * self.right


def parse_mul(s: str) -> Mul:
    start = s.index('(')
    stop = s.index(')')
    comma = s.index(',')
    l = int(s[start+1:comma])
    r = int(s[comma+1:stop])
    return Mul(l, r)


if __name__ == "__main__":
    d = Day(3)
    lines = d.read_lines()
    pattern = "mul\\([0-9]{1,3},[0-9]{1,3}\\)"
#    pattern = "mul([0-9]{1,3},[0-9]{1,3})"
    matches = map(parse_mul, flatten([re.findall(pattern, l) for l in lines]))
    print(sum(list([x.prod() for x in matches])))
