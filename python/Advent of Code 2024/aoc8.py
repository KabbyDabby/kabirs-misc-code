from aoc8input import test_input, actual_input
from collections import defaultdict
from math import gcd


def prod(*iter):
    ret = 1
    for x in iter:
        ret *= x
    return ret


def add_tuples(t1, t2):
    return tuple(x + y for x, y in zip(t1, t2))


def subtract_tuples(t1, t2):
    return tuple(x - y for x, y in zip(t1, t2))


def reduce_tuple(tup):
    reduction_factor = gcd(*tup)
    return tuple(x // reduction_factor for x in tup)


def part1(input):
    lines = input.strip().split("\n")
    unique_chars = set()
    for i in range(len(lines)):
        lines[i] = list(lines[i])
        for char in [c for c in lines[i] if c != "."]:
            unique_chars.add(char)

    frequency_locs = defaultdict(list)
    for char in unique_chars:
        for i, line in enumerate(lines):
            for j, loc in enumerate(line):
                if loc == char:
                    frequency_locs[char].append((i, j))

    antenna_locs = set()
    for char in frequency_locs.keys():
        temp = frequency_locs[char]
        if len(temp) == 1:
            continue
        for i, freq1 in enumerate(temp):
            for freq2 in temp[i + 1 :]:
                tuple1 = add_tuples(subtract_tuples(freq1, freq2), freq1)
                if 0 <= tuple1[0] < len(lines) and 0 <= tuple1[1] < len(lines[0]):
                    antenna_locs.add(tuple1)
                tuple2 = add_tuples(subtract_tuples(freq2, freq1), freq2)
                if 0 <= tuple2[0] < len(lines) and 0 <= tuple2[1] < len(lines[0]):
                    antenna_locs.add(tuple2)
    # print(f"antenna_locs: {antenna_locs}")
    # for i in range(len(lines)):
    #    for j in range(len(lines[i])):
    #        if (i, j) in antenna_locs:
    #            lines[i][j] = "#"
    #    print("".join(lines[i]))
    return len(antenna_locs)


# print(f"test: {part1(test_input)}")
# print(f"actual: {part1(actual_input)}")


def part2(input):
    lines = input.strip().split("\n")
    unique_chars = set()
    for i in range(len(lines)):
        lines[i] = list(lines[i])
        for char in [c for c in lines[i] if c != "."]:
            unique_chars.add(char)

    #    for line in lines:
    # print("".join(line))

    frequency_locs = defaultdict(list)
    for char in unique_chars:
        for i, line in enumerate(lines):
            for j, loc in enumerate(line):
                if loc == char:
                    frequency_locs[char].append((i, j))

    antenna_locs = set()
    for char in frequency_locs.keys():
        temp = frequency_locs[char]
        if len(temp) == 1:
            continue
        for i, freq1 in enumerate(temp):
            for freq2 in temp[i + 1 :]:
                diff = reduce_tuple(subtract_tuples(freq1, freq2))
                print(f"diff: {diff}")
                tuple1 = freq2
                while 0 <= tuple1[0] < len(lines) and 0 <= tuple1[1] < len(lines[0]):
                    antenna_locs.add(tuple1)
                    tuple1 = add_tuples(tuple1, diff)
                tuple1 = freq1
                while 0 <= tuple1[0] < len(lines) and 0 <= tuple1[1] < len(lines[0]):
                    antenna_locs.add(tuple1)
                    tuple1 = subtract_tuples(tuple1, diff)
    print(f"antenna_locs: {antenna_locs}")
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if (i, j) in antenna_locs:
                lines[i][j] = "#"
        print("".join(lines[i]))
    return len(antenna_locs)


print(f"test: {part2(test_input)}")
print(f"actual: {part2(actual_input)}")
