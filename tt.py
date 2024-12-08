from typing import Generator


def ops(n) -> Generator[list[str], None, None]:
    if n == 0:
        yield []
    else:
        for l in ops(n-1):
            yield ['+'] + l
            yield l + ['-']


if __name__ == "__main__":
    print(list(ops(3)))
