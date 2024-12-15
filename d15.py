from day import Day, split_list, flatten
from pt import pt, move_to_dir, N, E, S, W


def map_find(m: list[list[str]], needle: str) -> list[pt]:
    found = []
    for j, l in enumerate(m):
        for i, c in enumerate(l):
            if c == needle:
                found.append(pt(i, j))
    return found


def parse_p2(lines: list[str]) -> tuple[list[list[str]], pt, list[str]]:
    m, _, moves = parse(lines)

    def widen_char(c) -> list[str]:
        if c == '#':
            return ['#', '#']
        elif c == 'O':
            return ['[', ']']
        elif c == '.':
            return ['.', '.']
        elif c == '@':
            return ['@', '.']
        else:
            raise RuntimeError(f'Unrecognised char {c}')

    m = [flatten([widen_char(c) for c in row]) for row in m]
    robots = map_find(m, '@')
    if len(robots) != 1:
        raise RuntimeError(f'Logic error - more than one robot')
    return m, robots[0], moves


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


def is_box(c) -> bool:
    return c == '[' or c == ']'


def can_move_box(m, start, dir) -> bool:
    # print(f'can_move_box: {start} {dir}')
    # display_map(m)

    our_box = []
    c = start.char_at(m)
    if c == '[':
        our_box = [start, start + E]
    elif c == ']':
        our_box = [start + W, start]
    else:
        raise RuntimeError(f'logic error - found non-box char {c} at {start}')

    next_pts = [p + dir for p in our_box]
    if dir == E:
        next_pts = [next_pts[1]]
    if dir == W:
        next_pts = [next_pts[0]]

    next_cs = "".join([p.char_at(m) for p in next_pts])
    if '#' in next_cs:
        return False

    return all([can_move_box(m, p, dir) for p in next_pts if is_box(p.char_at(m))])


def move_box(m, start, dir):

    # We should have already checked
    ok = can_move_box(m, start, dir)
    if not ok:
        raise RuntimeError(f'Moving but cannot move')

    # Helper
    def move_char(fr, to):
        m[to.y][to.x] = fr.char_at(m)
        m[fr.y][fr.x] = '.'

    our_box = []
    c = start.char_at(m)
    if c == '[':
        our_box = [start, start + E]
    elif c == ']':
        our_box = [start + W, start]
    else:
        raise RuntimeError(f'logic error - found non-box char {c}')

    # We may have "all space", "space and box" or "some wall" in this direction
    dest_pts = [p + dir for p in our_box]
    check_pts = dest_pts[:]
    if dir == E:
        check_pts = [check_pts[1]]
    if dir == W:
        check_pts = [check_pts[0]]

    check_cs = "".join([p.char_at(m) for p in check_pts])
    if '#' in check_cs:
        raise RuntimeError(f'Should be able to move but wall in the way')

    if check_cs == '..' or check_cs == '.':
        if dir != E:
            move_char(our_box[0], dest_pts[0])
            move_char(our_box[1], dest_pts[1])
        else:
            move_char(our_box[1], dest_pts[1])
            move_char(our_box[0], dest_pts[0])
        return True

    if check_cs[0] == '[':
        move_box(m, check_pts[0], dir)
    if check_cs[0] == ']':
        move_box(m, check_pts[0], dir)
    if len(check_cs) == 2 and check_cs[1] == '[':
        move_box(m, check_pts[1], dir)

    check_cs = "".join([p.char_at(m) for p in check_pts])
    if not (check_cs == '..' or check_cs == '.'):
        raise RuntimeError(f'Error moving box out of the way ({check_cs})')

    if dir != E:
        move_char(our_box[0], dest_pts[0])
        move_char(our_box[1], dest_pts[1])
    else:
        move_char(our_box[1], dest_pts[1])
        move_char(our_box[0], dest_pts[0])


def apply_move_p2(m, robot, move):
    dir = move_to_dir(move)
    q = robot + dir
    c = q.char_at(m)

    if c == '#':
        # Moving into a wall
        return robot
    if c == '.':
        # Moving into a space
        m[q.y][q.x] = '@'
        m[robot.y][robot.x] = '.'
        return q
    if not is_box(c):
        raise RuntimeError(f'logic error - found char {c}')

    if can_move_box(m, q, dir):
        move_box(m, q, dir)

        m[q.y][q.x] = '@'
        m[robot.y][robot.x] = '.'
        robot = q

    return robot


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


def p2(lines: list[str]) -> int:
    m, robot, moves = parse_p2(lines)
    display_map(m)
    for move in moves:
        # print(f'Next move {move}')
        robot = apply_move_p2(m, robot, move)
        # print(f'Moved {move}')
        # display_map(m)
        # print(f'Robot {robot}')
        # print("")

    display_map(m)
    boxes = map_find(m, '[')

    return sum([gps_coord(box) for box in boxes])

    return 0


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
    print(p2(lines))
