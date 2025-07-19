import re
from aoc3input import test_input, actual_input

def part1(input):
    li = re.findall("mul\([0-9]+,[0-9]+\)",input)
    ret = 0
    for mul in li:
        temp = re.findall("[0-9]+",mul)
        ret += int(temp[0])*int(temp[1])
    return ret

def part2(input):
    li = re.findall("mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)",input)
    add = True
    ret = 0
    for mul in li:
        if mul == "do()":
            add = True
            continue
        elif mul == "don't()":
            add = False
            continue

        if add == True:
            temp = re.findall("[0-9]+",mul)
            ret += int(temp[0])*int(temp[1])
    return ret
print(part2(actual_input))