from day import Day, str_to_nums


def is_safe(l: list[int]):
    deltas = list(map(lambda x, y: x - y, l[1:], l[:-1]))
    good_size = all(map(lambda d: abs(d) >= 1 and abs(d) <= 3, deltas))
    monotonic = all(map(lambda d: d > 0, deltas)) or all(
        map(lambda d: d < 0, deltas))
    return monotonic and good_size


if __name__ == "__main__":
    d = Day(2)
    reports = [str_to_nums(l) for l in d.read_lines()]
#    for report in reports:
#        print(report, is_safe(report))
    print(len(list(filter(is_safe, reports))))
