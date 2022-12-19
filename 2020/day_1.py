# coding: utf-8
        
# Part 1
with open("data/1_input.txt") as fp:
    data = dict()
    for line in fp:
        value = int(line)
        complement = 2020-value
        if complement in data:
            print(value, complement, value+complement, value*complement)
        data[value] = complement
        
        
# Part 2
with open("data/1_input.txt") as fp:
    data = []
    for line in fp:
        data.append(int(line))

possible_sums = {v1+v2: (v1,v2) for i, v1 in enumerate(data) for v2 in data[i+1:]}

for v in data:
    c = 2020-v
    if c in possible_sums:
        v1, v2 = possible_sums[c]
        print(v, possible_sums[c], sum((v,v1,v2)))
        print(v*v1*v2)
        break