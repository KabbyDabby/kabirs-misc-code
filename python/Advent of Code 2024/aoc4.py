from aoc4input import test_input, actual_input


def part1(input):
    word_search = input.strip().splitlines()
    for i in range(len(word_search)):
        word_search[i] = list(word_search[i])

    #    print(word_search)
    def is_dir_match(x, y, right, down):
        if (
            x + 3 * right >= len(word_search)
            or x + 3 * right < 0
            or y + 3 * down >= len(word_search[0])
            or y + 3 * down < 0
        ):
            return False
        if word_search[x + right][y + down] != "M":
            return False
        if word_search[x + 2 * right][y + 2 * down] != "A":
            return False
        if word_search[x + 3 * right][y + 3 * down] != "S":
            return False
        return True

    def find_num_matches_at_char(x, y):
        num_matches = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if is_dir_match(x, y, i, j):
                    num_matches += 1
        return num_matches

    total_matches = 0

    for i, line in enumerate(word_search):
        for j, c in enumerate(line):
            if c == "X":
                total_matches += find_num_matches_at_char(i, j)
    return total_matches


# print("Test:", part1(test_input))
# print("Actual:", part1(actual_input))


def part2(input):
    word_search = input.strip().splitlines()
    for i in range(len(word_search)):
        word_search[i] = list(word_search[i])

    #    print(word_search)
    def is_char_match(x, y):
        if (
            x + 1 >= len(word_search)
            or x - 1 < 0
            or y + 1 >= len(word_search[0])
            or y - 1 < 0
        ):
            return False
        if not (
            word_search[x - 1][y - 1] == "M"
            and word_search[x + 1][y + 1] == "S"
            or word_search[x - 1][y - 1] == "S"
            and word_search[x + 1][y + 1] == "M"
        ):
            return False
        if not (
            word_search[x - 1][y + 1] == "M"
            and word_search[x + 1][y - 1] == "S"
            or word_search[x - 1][y + 1] == "S"
            and word_search[x + 1][y - 1] == "M"
        ):
            return False
        return True

    total_matches = 0

    for i, line in enumerate(word_search):
        for j, c in enumerate(line):
            if c == "A":
                total_matches += is_char_match(i, j)
    return total_matches


print("Test:", part2(test_input))
print("Actual:", part2(actual_input))
