from collections import Counter

def priority(x):
    p = ord(x)
    if ord("a") <= p <= ord("z"):
        return p - ord("a") + 1
    return p - ord("A") + 27

data = []
total = 0
with open("day03.txt") as fp:
    for line in fp:
        line = line.strip()
        data.append(line)
        N = len(line)//2
        first, second = Counter(line[:N]), Counter(line[N:])
        common = next(iter((first & second).keys()))
        total += priority(common)

print(f"{total=}")


total = 0
for i in range(0, len(data), 3):
    lines = data[i:i+3]
    common = set(lines[0])
    for line in lines[1:]:
        common &= set(line)
    common = list(common)[0]
    total += priority(common)

print(f"{total=}")