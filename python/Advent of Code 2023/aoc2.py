from aoc2input import test_string
from aoc2input import actual_input


def check(game):
    return (
        check_color("red", game)
        and check_color("blue", game)
        and check_color("green", game)
    )


def check_color(color, game):
    color_number = 0

    for c in range(len(game)):
        if game[c : c + len(color)] == color:
            print(color)
            if c - 4 >= 0 and game[c - 4].isnumeric():
                color_number = int(game[c - 4 : c - 1])
                print("game[c-4:c-1] = " + str(color_number))
                break
            elif c - 3 >= 0 and game[c - 3].isnumeric():
                color_number = int(game[c - 3 : c - 1])
                print("game[c-3:c-1] = " + str(color_number))
                break
            else:
                color_number = int(game[c - 2])
                print("game[c-2] = " + str(color_number))
                break

    if color == "red" and color_number <= 12:
        print("Red Works, color_number == " + str(color_number))
        return True
    if color == "green" and color_number <= 13:
        print("Blue Works, color_number == " + str(color_number))
        return True
    if color == "blue" and color_number <= 14:
        print("Green Works, color_number == " + str(color_number))
        return True
    return False


def count_color(color, game):
    for c in range(len(game)):
        if game[c : c + len(color)] == color:
            print(color)
            if c - 4 >= 0 and game[c - 4].isnumeric():
                print("game[c-4:c-1] = " + game[c - 4 : c - 1])
                return int(game[c - 4 : c - 1])
            elif c - 3 >= 0 and game[c - 3].isnumeric():
                print("game[c-3:c-1] = " + game[c - 3 : c - 1])
                return int(game[c - 3 : c - 1])
            else:
                print("game[c-2] = " + game[c - 2])
                return int(game[c - 2])
    return 0


def part1(input):
    lines = [x for x in input.split("\n")]
    line_total = 0
    for line in lines:
        if line[7].isdecimal():
            print("game_number = " + line[5:8])
            game_number = int(line[5:8])
        elif line[6].isdecimal():
            print("game_number = " + line[5:7])
            game_number = int(line[5:7])
        else:
            print("game_number = " + line[5])
            game_number = int(line[5])
        games = [y for y in line.split(";")]
        num_games_work = 0
        for game in games:
            if check(game):
                num_games_work += 1
        if num_games_work == len(games):
            line_total += game_number
    print(line_total)


def part2(input):
    lines = [x for x in input.split("\n")]
    power_total = 0
    for line in lines:
        games = [y for y in line.split(";")]
        min_red = 0
        min_blue = 0
        min_green = 0
        for game in games:
            if count_color("red", game) > min_red:
                min_red = count_color("red", game)
            if count_color("blue", game) > min_blue:
                min_blue = count_color("blue", game)
            if count_color("green", game) > min_green:
                min_green = count_color("green", game)

        power_total += min_red * min_blue * min_green
    print(power_total)


part1(test_string)

part1(actual_input)

part2(test_string)

part2(actual_input)
