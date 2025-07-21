from aoc5input import test_input, actual_input
from math import inf


def part1(input):
    rules, updates = input.strip().split("\n\n")
    rules = rules.splitlines()
    updates = updates.splitlines()

    rules = [(int(rule.split("|")[0]), int(rule.split("|")[1])) for rule in rules]

    for i in range(len(updates)):
        updates[i] = [int(num) for num in updates[i].split(",")]

    ret = 0

    for update in updates:
        locs = {}
        for i, item in enumerate(update):
            locs[item] = i

        for rule in rules:
            if locs.get(rule[0], -1) > locs.get(rule[1], inf):
                break
        else:
            ret += update[len(update) // 2]

    return ret


# print(f"test: { part1(test_input) }")
# print(f"actual: { part1(actual_input) }")


def part2(input):
    rules, updates = input.strip().split("\n\n")
    rules = rules.splitlines()
    updates = updates.splitlines()

    rules = [(int(rule.split("|")[0]), int(rule.split("|")[1])) for rule in rules]

    for i in range(len(updates)):
        updates[i] = [int(num) for num in updates[i].split(",")]

    ret = 0

    def find_middle_bad_line(update, first_recursion):
        locs = {}
        for i, item in enumerate(update):
            locs[item] = i

        for rule in rules:
            if locs.get(rule[0], -1) > locs.get(rule[1], inf):
                new_update = update
                new_update.pop(locs[rule[0]])
                new_update.insert(locs[rule[1]], rule[0])
                return find_middle_bad_line(new_update, False)
        else:
            return 0 if first_recursion else update[len(update) // 2]

    for update in updates:
        ret += find_middle_bad_line(update, True)
    return ret


print(f"test: { part2(test_input) }")
print(f"actual: { part2(actual_input) }")
