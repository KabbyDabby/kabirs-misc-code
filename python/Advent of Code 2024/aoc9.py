from aoc9input import test_input, actual_input


def part1(input):
    disk_map = [int(c) for c in input]
    files = disk_map[::2]
    empty_space = disk_map[1::2]
    total_empty_space = sum(empty_space)
    ret = ""
    i = 0
    while files:
        ret += str(i) * files.pop(0)
        i += 1
        while empty_space[0] != 0:
            if not files:
                break
            # print(f"files: {files}, empty_space: {empty_space}, i: {i}")
            # print(f"ret: {ret}")
            temp = min(empty_space[0], files[-1])
            ret += str(len(files) + i - 1) * temp
            empty_space[0] -= temp
            files[-1] -= temp
            if files[-1] == 0:
                files.pop(-1)

        empty_space.pop(0)
    ret = [int(c) for c in ret]
    return sum(map(lambda x, y: x * y, ret, range(len(ret))))


print(f"test: {part1(test_input)}")
print(f"actual: {part1(actual_input)}")


def part2(input):
    while True:
        print("Part 2 is not implemented yet.")
