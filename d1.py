from day import Day, str_to_nums, transpose, repeat_counts


if __name__ == "__main__":
    d = Day(1)
    lines = d.read_lines()
    rows = [str_to_nums(l) for l in lines]
    cols = transpose(rows)
    cols[0].sort()
    cols[1].sort()
    deltas = [abs(cols[0][i]-cols[1][i]) for i in range(len(cols[0]))]
    print(sum(deltas))

    counts = repeat_counts(cols[1])

    print(sum([l * counts.get(l, 0) for l in cols[0]]))
