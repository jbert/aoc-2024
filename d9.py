from day import Day, partition
from dataclasses import dataclass
from collections import deque
from copy import copy


@dataclass
class chunk:
    id: int | None
    start: int
    length: int

    def range(self) -> range:
        return range(self.start, self.start+self.length)

    def is_free(self) -> bool:
        return self.id is None

    def stop(self) -> int:
        return self.start + self.length


def parse_p1(s: str) -> tuple[dict[int, int | None], int]:
    sectors = {}
    digits = list(s)

    id = 0
    offset = 0
    is_file = True

    for digit in digits:

        this_id = None
        if is_file:
            this_id = id
            id += 1

        length = int(digit)

        for sid in range(offset, offset+length):
            sectors[sid] = this_id

        offset += length
        is_file = not is_file

    return sectors, offset-1


def sectors_to_str(sectors, max_sid):
    s = ""
    for i in range(0, max_sid+1):
        id = sectors[i]
        if id is None:
            s += '.'
        else:
            s += str(id)
    return s


def parse_p2(s: str) -> list[chunk]:
    digits = list(s)
    chunks = []

    id = 0
    offset = 0
    is_file = True

    for digit in digits:

        this_id = None
        if is_file:
            this_id = id
            id += 1

        length = int(digit)

        c = chunk(this_id, offset, length)
        if c.length > 0:
            chunks.append(c)

        offset += length
        is_file = not is_file

    return chunks


def sector_score(sectors, max_sid) -> int:
    score = 0
    for sid in range(0, max_sid+1):
        val = sectors[sid]
        if val is None:
            continue
        score += sid * val
    return score


def find_first_space(file, freelist) -> chunk | None:
    for c in freelist:
        if c.length >= file.length:
            return c
    return None


def freelist_insert(freelist, f):
    for i, c in enumerate(freelist):
        if f.start < c.start:
            freelist.insert(i, f)
            break


def p2(lines: list[str]) -> int:
    chunks = parse_p2(lines[0])

    freelist, files = partition(lambda c: c.is_free(), chunks)
    # Freelist in offset order
    freelist = deque(freelist)
    # Files are in file_id order, we adjust offsets but keep order (for now)
    files.reverse()
    for file in files:
        free = find_first_space(file, freelist)
        if free is None or free.start >= file.start:
            continue

#        print(f'Move {file} to {free}')

        new_free = copy(file)
        new_free.id = None

        file.start = free.start
        free.start = file.stop()
        free.length = free.length - file.length
        if free.length < 0:
            raise RuntimeError('logic error')
        if free.length == 0:
            #            print(f'removing {free}')
            freelist.remove(free)
        freelist_insert(freelist, new_free)
#        print(f'Moved {file} to {free}')

    sectors = {}
    max_sid = 0
    for c in files + list(freelist):
        #        print(f'range {c.range()} id {c.id}')
        for offset in c.range():
            sectors[offset] = c.id
            if offset > max_sid:
                max_sid = offset

    return sector_score(sectors, max_sid)


def p1(lines: list[str]) -> int:
    sectors, max_sid = parse_p1(lines[0])
#    print(f'sectors: {sectors}')
#    print(f'max_sid: {max_sid}')

    max_file_sid = max_sid
    for i in range(max_file_sid, 0, -1):
        #        print(f'i {i}')
        if not sectors[i] is None:
            max_file_sid = i
            break

    for sid in range(0, max_sid):
        #        print( f'sectors: {sectors_to_str(sectors, max_sid)} sid {sid} {sectors[sid]}')
        if not sectors[sid] is None:
            continue

        if sid >= max_file_sid:
            break

        # Move block
        sectors[sid] = sectors[max_file_sid]
        sectors[max_file_sid] = None

        for i in range(max_file_sid, 0, -1):
            if not sectors[i] is None:
                max_file_sid = i
                break
        if max_file_sid == 0:
            raise RuntimeError("No data?")

    return sector_score(sectors, max_file_sid)


if __name__ == "__main__":
    d = Day(9)
    lines = d.read_lines()
    print(p1(lines))
    print(p2(lines))
