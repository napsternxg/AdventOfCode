# https://adventofcode.com/2022/day/1


elf_calories = []
elf_calories_total = []
max_calories = 0
max_elf = -1

with open("day01.txt") as fp:
    c_list = fp.read().split("\n\n")
    for i, c in enumerate(c_list):
        c = c.strip()
        c = [int(x.strip()) for x in c.split()]
        elf_calories.append(c)
        elf_calories_total.append(sum(c))
        if elf_calories_total[-1] > max_calories:
            max_calories = elf_calories_total[-1]
            max_elf = i
print(elf_calories)
print(elf_calories_total)
sorted_cals = sorted(((x, i) for i, x in enumerate(elf_calories_total)), reverse=True)
print(sorted_cals)
print(max_calories)
print(f"{(max_elf+1)=}")

print(f"{sum([x for x, i in sorted_cals[:3]])=}")

