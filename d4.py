from copyreg import add_extension
from day import Day, flatten
from pt import pt


def p1(m: list[str]) -> int:

    locations: dict[str, set[pt]] = {}
    # Could do this in one pass, what is best way?
    for char in 'XMAS':
        locations[char] = set([pt(i, j) for j, l in enumerate(lines)
                               for i, c in enumerate(l) if c == char])

    paths: list[list[pt]] = list([[l] for l in locations['X']])
    next_paths = list()
    for char in 'MAS':
        #        print(f'char {char} num_paths {len(paths)}')
        for i, path in enumerate(paths):
            #    print(f'i {i} num_paths {len(paths)} lp {len(path)} path {path}')
            for p in locations[char]:
                #    print(f'p {p}')
                if path[-1].is_adjacent(p):
                    new_path = path[:]
                    new_path.append(p)
                    next_paths.append(new_path)
        paths = next_paths[:]

    print(len(paths))
    return 0


if __name__ == "__main__":
    d = Day(4)
    lines = d.read_lines()
    print(p1(lines))
