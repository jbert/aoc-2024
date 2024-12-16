from day import Day, flatten_los
from pt import pt, map_find, E, NESW
import sys


def parse(lines: list[str]) -> tuple[list[str], pt, pt]:
    start = map_find(lines, 'S')
    end = map_find(lines, 'E')
    if len(start) != 1 or len(end) != 1:
        raise RuntimeError(f'too many starts or ends')
    return lines, start[0], end[0]


#
# Was going to astar a graph based on the maze but realised
# that the cost to go from one pt to another isn't constant,
# since it depends on previous move
#
# class node(NamedTuple):
#    vid: str
#    adj: set[tuple[str, int]]
#
#    def to_pt(self):
#        return pt_parse(self.vid)
#
#
# class maze(NamedTuple):
#    start: pt
#    end: pt
#    nodes: dict[str, node]
#
#    def pt_to_node(self, p: pt) -> node:
#        return self.nodes[str(p)]
#
#
# def parse_map(start: pt, end: pt, m: list[str]) -> maze:
#    nodes = {}
#    pts = map_find(m, '.')
#    pts.append(start)
#    pts.append(end)
#    for p in pts:
#        adj = set(p.adjacent_pts_nesw())
#        for a in adj.intersection(pts):
#
#    return maze(start, end, nodes)


def calc_turns(cur: pt, new: pt) -> int:
    if cur == new:
        return 0
    if cur == pt(0, 0)-new:
        return 2
    return 1


def maze_solve(spaces: set[pt], p: pt, end: pt, seen: dict[pt, int], dr: pt) -> tuple[int, list[pt]] | None:
    print(f'MS: p {p}')
    if p == end:
        return 0, []

    adj_spaces = set(p.adjacent_pts_nesw()).intersection(spaces)
    seen_pts = set([p for p, c in seen.items() if c > 0])
    print(seen_pts)
    neighbours = adj_spaces - seen_pts

    cost_paths = []

    c = seen.get(p, 0)
    seen[p] = c + 1
    for neighbour in neighbours:
        new_dr = neighbour - p
        cost_path = maze_solve(spaces, neighbour, end, seen, new_dr)
        if cost_path is None:
            continue
        n_cost, path = cost_path

        n_cost += 1 + calc_turns(dr, new_dr) * 1000
        cost_paths.append((n_cost, [neighbour] + path))
    seen[p] -= 1

    if len(cost_paths) == 0:
        return None

    cost_paths.sort(key=lambda t: t[0])
    return cost_paths[0]


def display_path(lines: list[str], lpath: list[pt]):
    path = set(lpath)
    for j, line in enumerate(lines):
        pline = ""
        for i, c in enumerate(line):
            p = pt(i, j)
            if p in path:
                c = 'X'
            pline += c
        print(pline)

# works on test cases:
# 441440 - too high
# 349168 - too high


def p1(lines: list[str]) -> int:
    sys.setrecursionlimit(20000)

    maze, start, end = parse(lines)
    spaces = map_find(maze, '.') + [start, end]
#    cost_path = maze_solve(set(spaces), start, end, set(), E)
    cost_path = maze_solve(set(spaces), start, end, {}, E)
    if cost_path is None:
        raise RuntimeError("can't solve")
    cost, path = cost_path
    display_path(lines, path)
    return cost


if __name__ == "__main__":
    d = Day(16)
    lines = d.read_lines()
    print(p1(lines))
