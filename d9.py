from day import Day, partition
from dataclasses import dataclass
from collections import deque


# @dataclass
# class chunk:
#    id: int | None
#    start: int
#    length: int
#
#    def range(self) -> range:
#        return range(self.start, self.start+self.length)
#
#    def is_free(self) -> bool:
#        return self.id is None


def parse(s: str) -> tuple[dict[int, int | None], int]:
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


# def parse(s: str) -> list[chunk]:
#    digits = list(s)
#    chunks = []
#
#    id = 0
#    offset = 0
#    is_file = True
#
#    for digit in digits:
#
#        this_id = None
#        if is_file:
#            this_id = id
#            id += 1
#
#        length = int(digit)
#
#        c = chunk(this_id, offset, length)
#        if c.length > 0:
#            chunks.append(c)
#
#        offset += length
#        is_file = not is_file
#
#    return chunks

def sector_score(sectors, max_file_sid) -> int:
    score = 0
    for sid in range(0, max_file_sid+1):
        score += sid * sectors[sid]
    return score


def p1(lines: list[str]) -> int:
    #    chunks = parse(lines[0])
    #
    #    freelist, files = partition(lambda c: c.is_free(), chunks)
    #    freelist = deque(freelist)
    #    for len(freelist) > 1:
    #        f = freelist[0]
    #        # invariant:
    #        # beginning of freelist is nonzero
    #        # end of file list is nonzero
    #
    #        # Move one sector
    #
    #        # Make space
    #        f.start += 1
    #        f.length -= 1
    sectors, max_sid = parse(lines[0])
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
