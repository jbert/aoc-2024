import random
import time

tcache: dict[tuple[int,int],int] = {}
dcache: dict[int,dict[int,int]] = {}

num_entries = 10 * 1000 * 1000
random.seed(0)

fact = 0.1

before = time.time()
for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))
    c = random.randint(0, int(num_entries * fact))
for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))

after = time.time()
dur = after-before
print(f"pure getrandom took {dur} seconds - {num_entries/dur} entries/sec")

before = time.time()
for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))
    c = random.randint(0, int(num_entries * fact))
    tcache[(a,b)] = c
for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))
    _ = tcache.get((a,b), None)

after = time.time()
dur = after-before
print(f"tuple cache took {dur} seconds - {num_entries/dur} entries/sec")

before = time.time()
for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))
    c = random.randint(0, int(num_entries * fact))
    d = tcache.get(a, {})
    d[b] = c
    tcache[a] = d

for i in range(0, num_entries):
    a = random.randint(0, int(num_entries * fact))
    b = random.randint(0, int(num_entries * fact))
    d = dcache.get(a, {})
    _ = d.get(b, None)

after = time.time()
dur = after-before
print(f"dict-dict cache took {dur} seconds - {num_entries/dur} entries/sec")
