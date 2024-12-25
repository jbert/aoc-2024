from day import Day, split_list

def fit(key, lock):
    for i, k in enumerate(key):
        if k + lock[i] > 5:
            return False
    return True

def parse_key(chunk):
    key = []
    for i in range(len(chunk[0])):
        for j in range(len(chunk)):
            if chunk[len(chunk) - j - 1][i] == '.':
                key.append(j-1)
                break
    return key

def parse_lock(chunk):
    lock = []
    for i in range(len(chunk[0])):
        for j in range(len(chunk)):
            if chunk[j][i] == '.':
                lock.append(j-1)
                break
    return lock

def parse(lines):
    chunks = split_list(lambda l: l == "", lines)
    keys = []
    locks = []
    for chunk in chunks:
        if chunk[0][0] == '#':
            locks.append(parse_lock(chunk))
        else:
            keys.append(parse_key(chunk))
    return keys, locks

def p1(lines: list[str]) -> int:
    keys, locks = parse(lines)
    print(keys)
    print(locks)
    count = 0
    for key in keys:
        for lock in locks:
            if fit(key, lock):
                count += 1
    return count


if __name__ == "__main__":
    d = Day(25)
    lines = d.read_lines()
    print(p1(lines))
