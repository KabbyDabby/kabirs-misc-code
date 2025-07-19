from aoc1input import test_input, actual_input

def part1(input):
    masses = [int(n) for n in input.split()]

    ret = 0

    for mass in masses:
        ret+=(mass//3)-2

    return ret

def part2(input):
    masses = [int(n) for n in input.split()]

    ret = 0

    for mass in masses:
        fuel = (mass//3)-2

        while fuel>0:
            ret+=fuel
            fuel = (fuel//3)-2

    return ret

# print(part1(actual_input))

print(part2(actual_input))

