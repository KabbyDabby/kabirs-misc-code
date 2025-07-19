from aoc3input import test_input, actual_input, actual_actual_input

def part1(input):
    wire1, wire2 = input.split('\n')
    wire1, wire2 = wire1.split(','), wire2.split(',')
    path = set()
    pos = (0,0)
    for instruction in wire1:
        axis = 0
        dir = 1
        if instruction[0] == 'L':
            dir = -1
        elif instruction[0] == 'U':
            axis = 1
        elif instruction[0] == 'D':
            axis = 1
            dir = -1

        for i in range(int(instruction[1:])):
            pos = (pos[0]+dir, pos[1]) if axis == 0 else (pos[0], pos[1]+dir)
            path.add(pos)

    pos = [0,0]
    ret = float('inf')
    for instruction in wire2:
        axis = 0
        dir = 1
        if instruction[0] == 'L':
            dir = -1
        elif instruction[0] == 'U':
            axis = 1
        elif instruction[0] == 'D':
            axis = 1
            dir = -1
        
        for i in range(int(instruction[1:])):
            pos = (pos[0]+dir, pos[1]) if axis == 0 else (pos[0], pos[1]+dir)
            if pos in path:
                ret = min(ret, pos[0]+pos[1])


    return ret

def part2(input):
    wire1, wire2 = input.split('\n')
    wire1, wire2 = wire1.split(','), wire2.split(',')
    path = set()
    dist = {}
    pos = (0,0)
    count = 0
    for instruction in wire1:
        axis = 0
        dir = 1
        if instruction[0] == 'L':
            dir = -1
        elif instruction[0] == 'U':
            axis = 1
        elif instruction[0] == 'D':
            axis = 1
            dir = -1

        for i in range(int(instruction[1:])):
            count+=1
            pos = (pos[0]+dir, pos[1]) if axis == 0 else (pos[0], pos[1]+dir)
            if pos not in path:
                dist[pos] = count
            path.add(pos)
            

    pos = [0,0]
    ret = float('inf')
    count = 0
    for instruction in wire2:
        axis = 0
        dir = 1
        if instruction[0] == 'L':
            dir = -1
        elif instruction[0] == 'U':
            axis = 1
        elif instruction[0] == 'D':
            axis = 1
            dir = -1
        
        for i in range(int(instruction[1:])):
            count += 1
            pos = (pos[0]+dir, pos[1]) if axis == 0 else (pos[0], pos[1]+dir)
            if pos in path:
                ret = min(ret, dist[pos]+count)



    return ret


print(part2(actual_actual_input))
        
