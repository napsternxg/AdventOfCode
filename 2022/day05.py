import re

with open("day05.txt") as fp:
    lines, moves = fp.read().split("\n\n")
    lines = lines.splitlines()
    num_crates = len(re.split(r"\s+", lines[-1].strip()))
    print(num_crates)
    crates = [[] for i in range(num_crates)]
    for line in reversed(lines[:-1]):
        # line = line.split(" ")
        # print(len(line), line)
        line = [line[i : i + 4].strip() for i in range(0, len(line), 4)]
        for i, c in enumerate(line):
            crates[i].append(c[1:-1]) if c.strip() else None
        # crates = [[c[1:-1] for c in line.split()] ]

print(num_crates)
print(crates)


def print_crates(crates):
    for i, c in enumerate(crates, start=1):
        print(i, c)


print_crates(crates)


def move_crates(n, f, t, same_order=False):
    crates[f], to_move = crates[f][:-n], crates[f][-n:]
    if not same_order:
        to_move = reversed(to_move)
    crates[t].extend(to_move)
    # crates[f] = crates[f][:-n]


MOVE_REGEX = re.compile(r"move ([\d]+) from ([\d]+) to ([\d]+)")
for line in moves.splitlines():
    # print(line)
    line = MOVE_REGEX.findall(line)[0]
    # print(line)
    n, f, t = [int(x) for x in line]
    # print(n, f, t)
    move_crates(n, f - 1, t - 1, same_order=True)  # part 2 = True
    # print_crates(crates)
    # break

print_crates(crates)

tops = "".join(c[-1] for c in crates)
print(tops)
