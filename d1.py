from day import Day, str_to_nums, transpose


if __name__ == "__main__":
    d = Day(1)
    lines = d.read_lines()
    rows = [str_to_nums(l) for l in lines]
    cols = transpose(rows)
    cols[0].sort()
    cols[1].sort()
    deltas = [abs(cols[0][i]-cols[1][i]) for i in range(len(cols[0]))]
    print(sum(deltas))

    counts = {}
    last_c = None
    last_count = 0
    for c in cols[1]:
        if last_c is not None:
            if c == last_c:
                last_count += 1
            else:
                counts[last_c] = last_count
                last_c = c
                last_count = 1
        else:
            last_c = c
            last_count = 1
    counts[last_c] = last_count

    print(sum([l * counts.get(l, 0) for l in cols[0]]))
