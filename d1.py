from day import Day, str_to_nums, transpose


if __name__ == "__main__":
    d = Day(1)
    lines = d.read_lines()
    rows = [str_to_nums(l) for l in lines]
    cols = transpose(rows)
    cols[0].sort()
    cols[1].sort()
    # print(cols)
    # print(cols[0])
    deltas = [abs(cols[0][i]-cols[1][i]) for i in range(len(cols[0]))]
    # print(deltas)

    # print(deltas)
    print(sum(deltas))
