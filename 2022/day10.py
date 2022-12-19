def get_cmd_cycles(line, x, cycle):
    if line[0] == "noop":
        cycle += 1
        yield x, cycle
        return
    if line[0] == "addx":
        cycle += 1
        yield x, cycle
        cycle += 1
        yield x + int(line[1]), cycle


def process_cycles(fp, verbose=False):
    cycle = 0
    x = 1
    ans = 0
    CRT = [["."] * 40 for i in range(6)]
    sprite = ["."] * 40
    sprite[0:3] = ["#", "#", "#"]
    sprite_mid = 1
    checkpoints = {20, 60, 100, 140, 180, 220}
    for line in fp:
        line = line.strip().split(" ")
        for new_x, cycle in get_cmd_cycles(line, x, cycle):
            signal_strength = cycle * x
            if verbose:
                print(f"{cycle=:>3d}, {line=}, {x=}, {signal_strength=}, {ans=}")
            if cycle in checkpoints:
                ans += signal_strength
            row, col = divmod(cycle - 1, 40)
            sprite_start = x - 1
            sprite_end = x + 1
            if sprite_start <= col <= sprite_end:
                CRT[row][col] = "#"
            x = new_x
            # if cycle > max(checkpoints):
            #     break
    return ans, CRT


test_input = """noop
addx 3
addx -5""".splitlines()

ans, CRT = process_cycles(test_input, verbose=True)
print(f"{ans=}")

import matplotlib.pyplot as plt

for input_file in ["day10-test.txt", "day10.txt"]:
    with open(input_file) as fp:
        print(f"{input_file=}")
        ans, CRT = process_cycles(fp, verbose=False)
        print(f"{ans=}")
        heatmap = []
        for row in CRT:
            print("".join(row))
            heatmap.append([int(x == "#") for x in row])
plt.imshow(heatmap)
plt.show()
