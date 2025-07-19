from math import inf
import heapq

def opp(dir):
    if dir == 'left':
        return 'right'
    elif dir == 'right':
        return 'left'
    elif dir == 'up':
        return 'down'
    elif dir == 'down':
        return 'up'
    else:
        return None

def next_pos(pos, dir):
    if dir == 'right':
        return (pos[0], pos[1] + 1)
    elif dir == 'down':
        return (pos[0] + 1, pos[1])
    elif dir == 'left':
        return (pos[0], pos[1] - 1)
    elif dir == 'up':
        return (pos[0] - 1, pos[1])
    else:
        raise ValueError("Invalid direction")

def part1(input):
    rows = input.strip().split('\n')
    n, m = len(rows), len(rows[0])
    grid = [[int(rows[i][j]) for j in range(m)] for i in range(n)]

    pq = [(0, (0, 0), None, 0)]  # (cost, (x, y), direction, steps in direction)
    dist = {(i, j, d, s): inf for i in range(n) for j in range(m) for d in ['up', 'down', 'left', 'right', None] for s in range(4)}
    dist[(0, 0, None, 0)] = 0

    prev = {}
    visited = set()

    while pq:
        cost, pos, dir, steps = heapq.heappop(pq)

        if pos == (n - 1, m - 1):
            path = []
            while pos != (0, 0):
                path.append(pos)
                pos, dir = prev[(pos, dir)]
            path.append((0, 0))
            path.reverse()
            return cost, path

        if (pos, dir, steps) in visited:
            continue
        visited.add((pos, dir, steps))

        for new_dir in ['up', 'right', 'down', 'left']:
            if dir is not None and new_dir == opp(dir):
                continue

            new_pos = next_pos(pos, new_dir)
            if 0 <= new_pos[0] < n and 0 <= new_pos[1] < m:
                new_cost = cost + grid[new_pos[0]][new_pos[1]]
                new_steps = steps + 1 if new_dir == dir else 1

                if new_steps <= 3 and new_cost < dist[(new_pos[0], new_pos[1], new_dir, new_steps)]:
                    dist[(new_pos[0], new_pos[1], new_dir, new_steps)] = new_cost
                    heapq.heappush(pq, (new_cost, new_pos, new_dir, new_steps))
                    prev[(new_pos, new_dir)] = (pos, dir)

    return inf, []

# Test with the example provided
input = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""

cost, path = part1(input)  # Expected output: 102
print("Cost:", cost)
print("Path:", path)
