MOVES = {
    "L": lambda i, j, n: (i, j - n),
    "R": lambda i, j, n: (i, j + n),
    "U": lambda i, j, n: (i - n, j),
    "D": lambda i, j, n: (i + n, j),
}


def sign(x):
    return 0 if x == 0 else abs(x) // x


def dist(head, tail):
    hi, hj = head
    ti, tj = tail
    dx = hi - ti
    dy = hj - tj
    d = max(abs(dx), abs(dy))
    grad = [sign(dx), sign(dy)]
    return d, grad


def make_grid(fp, rope_len=2):
    hi, hj = 0, 0
    ti, tj = hi, hj
    maxes = [hi, hj]
    mins = [hi, hj]
    tail_positions = []
    knot_positions = [(hi, hj) for i in range(rope_len)]  # Non head knots
    # unique_tails = set()
    for line in fp:
        dir, n = line.strip().split(" ")
        n = int(n)
        for step in range(n):
            tail_positions.append((ti, tj))
            hi, hj = MOVES[dir](hi, hj, 1)
            knot_positions[0] = (hi, hj)
            for i in range(1, rope_len):
                pki, pkj = knot_positions[i - 1]
                ki, kj = knot_positions[i]
                d, (gi, gj) = dist((pki, pkj), (ki, kj))
                if d > 1:  # Only move knot if dist(leading_knot, knot) > rope_len
                    ki, kj = ki + gi, kj + gj
                knot_positions[i] = ki, kj
            ti, tj = knot_positions[-1]
        # print(f"{ti=}, {tj=}, {dir=}, {n=}, {hi=}, {hj=}")
        maxes = [max(x, c) for x, c in zip(maxes, (hi, hj))]
        mins = [min(x, c) for x, c in zip(mins, (hi, hj))]
    tail_positions.append((ti, tj))
    print(f"{rope_len=}, {maxes=}, {mins=}")
    # print(f"{tail_positions=}")
    print(f"{len(set(tail_positions))=}")


input_file = "day09.txt"

with open(input_file) as fp:
    make_grid(fp, rope_len=2)

with open(input_file) as fp:
    make_grid(fp, rope_len=10)
