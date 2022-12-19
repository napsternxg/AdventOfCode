def has_overlap(first, second):
    if first[0] <= second[0] and first[1] >= second[1]:
        return True
    elif second[0] <= first[0] and second[1] >= first[1]:
        return True
    return False


def has_anyoverlap(first, second):
    if second[0] >= first[0] and second[0] <= first[1]:
        return True
    elif first[0] >= second[0] and first[0] <= second[1]:
        return True
    return False

overlaps = 0
any_overlaps = 0
with open("day04.txt") as fp:
    for line in fp:
        first, second = line.strip().split(",")
        first = [int(x) for x in first.split("-")]
        second = [int(x) for x in second.split("-")]
        overlaps += int(has_overlap(first, second))
        any_overlaps += int(has_anyoverlap(first, second))

print(f"{overlaps=}")
print(f"{any_overlaps=}")

