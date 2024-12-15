from day import Day, split_list, flatten
from pt import pt, move_to_dir


def map_find(m: list[list[str]], needle: str) -> list[pt]:
    found = []
    for j, l in enumerate(m):
        for i, c in enumerate(l):
            if c == needle:
                found.append(pt(i, j))
    return found


def parse(lines: list[str]) -> tuple[list[list[str]], pt, list[str]]:
    bits = split_list(lambda l: l == "", lines)
    m = [list(b) for b in bits[0]]
    robots = map_find(m, '@')
    if len(robots) != 1:
        raise RuntimeError(f'Logic error - more than one robot')
    return m, robots[0], flatten(flatten(bits[1:]))


def display_map(m: list[list[str]]):
    for row in m:
        l = "".join(row)
        print(l)


def apply_move(m, robot, move):
    dir = move_to_dir(move)
    q = robot + dir
    c = q.char_at(m)

    if c == '#':
        # Moving into a wall
        return robot
    if c == '.':
        # Moving into a space
        #        print(f'Move into space robot {robot} q {q} dir {dir}')
        m[q.y][q.x] = '@'
        m[robot.y][robot.x] = '.'
        return q
    if c != 'O':
        raise RuntimeError(f'logic error - found char {c}')

    # Look for first space or wall in this direction
    while q.char_at(m) == 'O':
        q += dir
    c = q.char_at(m)
    if c == '#':
        # We can't move
        return robot
    if c != '.':
        raise RuntimeError(f'logic error - found char {c}')
    # We had a box at the start, we have found a space
    # suffle a box across and move the robot
    m[q.y][q.x] = 'O'
    q = robot + dir
    m[q.y][q.x] = '@'
    m[robot.y][robot.x] = '.'
    return q


def gps_coord(p: pt) -> int:
    return p.x + p.y * 100


def p1(lines: list[str]) -> int:
    m, robot, moves = parse(lines)
#    print(m)
#    print(robot)
#    print(moves)

    for move in moves:
        # print(f'Next move {move}')
        # print(f'Robot {robot}')
        # display_map(m)
        robot = apply_move(m, robot, move)
        # print("")

    display_map(m)
    boxes = map_find(m, 'O')

    return sum([gps_coord(box) for box in boxes])


if __name__ == "__main__":
    d = Day(15)
    lines = d.read_lines()
    print(p1(lines))
