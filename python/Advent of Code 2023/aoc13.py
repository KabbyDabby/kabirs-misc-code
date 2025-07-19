from aoc13input import actual_input, test_input, test_input2


def check_symmetry(list):
    for i in range(1, len(list)):
        repeats = min(i, len(list) - i)
        print(f"repeats = {repeats}")

        for j in range(repeats):
            if list[i + j] != list[i - 1 - j]:
                print(f"list[i+j] = {list[i+j]}")  # prints breaking values
                print(f"list[i-1-j] = {list[i-1-j]}")
                break
        else:
            return i

    return -1


def check_symmetry_smudge(list):
    for i in range(1, len(list)):
        counter = 0
        repeats = min(i, len(list) - i)
        print(f"repeats = {repeats}")

        for j in range(repeats):
            if list[i + j] != list[i - 1 - j]:
                print(f"list[i+j] = {list[i+j]}")  # prints breaking values
                print(f"list[i-1-j] = {list[i-1-j]}")
                counter2 = 0
                for k in range(len(list[i + j])):
                    if list[i + j][k] != list[i - 1 - j][k]:
                        counter2 += 1
                    if counter2 > 1:
                        break
                if counter2 > 1:
                    break
                else:
                    counter += counter2
        else:
            print(f"counter = {counter}")
            if counter == 1:
                return i

    return -1


def part1(input):
    fields = input.split("\n\n")

    # print(fields)

    total = 0
    for field in fields:
        rows = field.split("\n")

        # print(rows)

        columns = []
        for i in range(len(rows[0])):
            column = ""
            for j in range(len(rows)):
                column += rows[j][i]
            columns.append(column)

        row_symmetry = check_symmetry(rows)
        print(f"Row symmetry is at {row_symmetry}")
        column_symmetry = check_symmetry(columns)
        print(f"Columns symmetry is at {column_symmetry}")

        if row_symmetry != -1:
            total += 100 * row_symmetry
        else:
            total += column_symmetry

    print(total)


def part2(input):
    fields = input.split("\n\n")

    # print(fields)

    total = 0
    for field in fields:
        rows = field.split("\n")

        # print(rows)

        columns = []
        for i in range(len(rows[0])):
            column = ""
            for j in range(len(rows)):
                column += rows[j][i]
            columns.append(column)

        row_symmetry = check_symmetry_smudge(rows)
        print(f"Row symmetry is at {row_symmetry}")
        column_symmetry = check_symmetry_smudge(columns)
        print(f"Columns symmetry is at {column_symmetry}")

        if row_symmetry != -1:
            total += 100 * row_symmetry
        else:
            total += column_symmetry

    print(total)


# part1(test_input)
# part1(test_input2)


# part1(actual_input)


# part2(test_input)
# part2(test_input2)


part2(actual_input)
