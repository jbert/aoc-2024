from day import Day, flatten
from typing import NamedTuple
import re


class Mul(NamedTuple):
    left: int
    right: int

    def prod(self) -> int:
        return self.left * self.right


class Dont:
    pass


class Do:
    pass


Tok = Do | Dont | Mul


def parse_mul(s: str) -> Mul:
    start = s.index('(')
    stop = s.index(')')
    comma = s.index(',')
    l = int(s[start+1:comma])
    r = int(s[comma+1:stop])
    return Mul(l, r)


def parse(s: str) -> Tok:
    if s.startswith('don'):
        return Dont()
    elif s.startswith('do'):
        return Do()
    else:
        return parse_mul(s)


def p1(lines: list[str]) -> int:
    pattern = "mul\\([0-9]{1,3},[0-9]{1,3}\\)"
#    pattern = "mul([0-9]{1,3},[0-9]{1,3})"
    matches = map(parse_mul, flatten([re.findall(pattern, l) for l in lines]))
    return sum(list([x.prod() for x in matches]))


def filter_tokens(tokens: list[Tok]) -> list[Mul]:
    ret = []
    enabled = True
    for tok in tokens:
        if type(tok) is Dont:
            enabled = False
        elif type(tok) is Do:
            enabled = True
        else:
            if enabled:
                ret.append(tok)
    return ret


def p2(lines: list[str]) -> int:
    #    lines = [
    #    '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))''']
    pattern = "(mul\\([0-9]{1,3},[0-9]{1,3}\\)|don't()|do())"
    tuple_matches = flatten([re.findall(pattern, l) for l in lines])
    matches = list(map(parse, [m[0] for m in tuple_matches]))
    nums = [x.prod() for x in filter_tokens(matches)]
    return sum(nums)


if __name__ == "__main__":
    d = Day(3)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
