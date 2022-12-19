def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return left - right
    if isinstance(left, int):
        left = [left]
    if isinstance(right, int):
        right = [right]
    for l, r in zip(left, right):
        c = compare(l, r)
        if c != 0:
            return c
    return len(left) - len(right)


from functools import cmp_to_key

from utils import DayInfo

day_info = DayInfo(__file__)

for input_file in day_info.input_files:
    print(f"==== {input_file.name=} ====")
    packets = []
    with open(input_file) as fp:
        data = fp.read().split("\n\n")
        ordered_pairs = []

        for i, pairs in enumerate(data, start=1):
            left, right = [eval(line.strip()) for line in pairs.splitlines()]
            packets.extend([left, right])
            if compare(left, right) <= 0:
                ordered_pairs.append(i)
        ans = sum(ordered_pairs)
        print(f"{ans=}, {ordered_pairs=}")
    packets.extend([[[2]], [[6]]])
    original_divider_pos = [len(packets) - 2, len(packets) - 1]

    sorted_packets = list(
        sorted(enumerate(packets), key=cmp_to_key(lambda x, y: compare(x[1], y[1])))
    )
    divider_pos = []
    for si, (i, packet) in enumerate(sorted_packets):
        if i in original_divider_pos:
            divider_pos.append(si + 1)
    print(f"{divider_pos=}")
    ans2 = divider_pos[0] * divider_pos[1]
    print(f"{ans2=}")
