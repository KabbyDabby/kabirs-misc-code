from aoc6input import test_input, actual_input
from collections import defaultdict


class directed_tuple:
    def __init__(self, position: tuple, direction: tuple):
        self.position = position
        self.direction = direction

    def turn(self):
        if self.direction == (0, 1):
            self.direction = (1, 0)
        elif self.direction == (1, 0):
            self.direction = (0, -1)
        elif self.direction == (0, -1):
            self.direction = (-1, 0)
        elif self.direction == (-1, 0):
            self.direction = (0, 1)

    def advance(self):
        self.position = (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )

    def undo_advance(self):
        self.position = (
            self.position[0] - self.direction[0],
            self.position[1] - self.direction[1],
        )

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def is_valid(self, grid):
        x, y = self.position
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            return True
        return False

    def is_obstacle(self, grid):
        x, y = self.position
        if grid[x][y] == "#":
            return True
        return False

    @staticmethod
    def get_next_dir(direction):
        if direction == (0, 1):
            return (1, 0)
        elif direction == (1, 0):
            return (0, -1)
        elif direction == (0, -1):
            return (-1, 0)
        elif direction == (-1, 0):
            return (0, 1)
        else:
            raise ValueError("Invalid direction")

    def __repr__(self):
        return f"Location: {self.position}, Direction: {self.direction}"


def part1(input):
    grid = input.strip().splitlines()
    for i in range(len(grid)):
        grid[i] = list(grid[i])

    #    print(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ">":
                loc = directed_tuple((i, j), (0, 1))
                break
            if grid[i][j] == "<":
                loc = directed_tuple((i, j), (0, -1))
                break
            if grid[i][j] == "v":
                loc = directed_tuple((i, j), (1, 0))
                break
            if grid[i][j] == "^":
                loc = directed_tuple((i, j), (-1, 0))
                break
        else:
            continue
        break
    else:
        raise ValueError("Start direction not found in grid")
    past_locs = set()
    while loc.is_valid(grid):
        past_locs.add(loc.get_position())
        # grid[loc.get_position()[0]][loc.get_position()[1]] = "X"
        loc.advance()
        while loc.is_valid(grid) and loc.is_obstacle(grid):
            loc.undo_advance()
            loc.turn()
            loc.advance()
    # for line in grid:
    #    print("".join(line))
    return len(past_locs)


# print(f"test: {part1(test_input)}")
# print(f"actual: {part1(actual_input)}")


def part2(input):
    grid = input.strip().splitlines()
    for i in range(len(grid)):
        grid[i] = list(grid[i])

    #    print(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ">":
                loc = directed_tuple((i, j), (0, 1))
                break
            if grid[i][j] == "<":
                loc = directed_tuple((i, j), (0, -1))
                break
            if grid[i][j] == "v":
                loc = directed_tuple((i, j), (1, 0))
                break
            if grid[i][j] == "^":
                loc = directed_tuple((i, j), (-1, 0))
                break
        else:
            continue
        break
    else:
        raise ValueError("Start direction not found in grid")
    past_locs = set()
    loc_dirs = defaultdict(set)
    ret = 0
    while loc.is_valid(grid):
        if not loc.get_position() in past_locs:
            past_locs.add(loc.get_position())
        else:
            # print(loc_dirs)
            print(f"{loc}, prev_dirs: {loc_dirs[loc.get_position()]}")
            if directed_tuple.get_next_dir(loc.get_direction()) in loc_dirs.get(
                loc.get_position(), set()
            ):
                loc.advance()
                if loc.is_valid(grid) and not loc.is_obstacle(grid):
                    ret += 1
                loc.undo_advance()
        loc_dirs[loc.get_position()].add(loc.get_direction())
        # grid[loc.get_position()[0]][loc.get_position()[1]] = "X"
        loc.advance()
        while loc.is_valid(grid) and loc.is_obstacle(grid):
            loc.undo_advance()
            loc.turn()
            loc.advance()
    # for line in grid:
    #    print("".join(line))
    return ret


print(f"test: {part2(test_input)}")
# print(f"actual: {part2(actual_input)}")
# give up for now :(
