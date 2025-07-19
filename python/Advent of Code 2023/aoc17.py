from aoc17input import test_input, actual_input, baby_input
from math import inf

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
        print("opp didn't work fix your goddamn code")


def cw(dir):
    if dir == 'left':
        return 'up'
    elif dir == 'up':
        return 'right'
    elif dir == 'right':
        return 'down'
    elif dir == 'down':
        return 'left'
    else:
        print("cw didn't work fix your goddamn code")

def ccw(dir):
    if dir == 'left':
        return 'down'
    elif dir == 'down':
        return 'right'
    elif dir == 'right':
        return 'up'
    elif dir == 'up':
        return 'left'
    else:
        print("ccw didn't work fix your goddamn code")


def next_pos(pos, dir):
    if dir == 'right':
        return (pos[0]+1, pos[1])
    elif dir == 'down':
        return (pos[0], pos[1]+1)
    elif dir == 'left':
        return (pos[0]-1, pos[1])
    elif dir == 'up':
        return (pos[0], pos[1]-1)
    else:
        print("next_pos didn't work fix your goddamn code")

def check(pos, dir, explored, dist, map, prev, columns, unexplored_dist, prev_dir_list):
    pf_pos = next_pos(pos,dir)

    # print(f'current pos = {pos}, potential next dir = {dir}, pf_pos = {pf_pos}')

    if pf_pos[0] < 0 or pf_pos[0] > len(columns)-1 or pf_pos[1] < 0 or pf_pos[1] > len(columns[0])-1:
        return inf
    

    elif pf_pos in explored:
        return inf
    else:
        if dist[pos] + map[pf_pos] < dist[pf_pos]:
            dist[pf_pos] = dist[pos] + map[pf_pos]
            unexplored_dist[pf_pos] = dist[pos] + map[pf_pos]
            prev[pf_pos] = pos
            prev_dir_list[pf_pos] = dir
        # print(f'also, the value at {pf_pos} is {map[pf_pos]} but the shortest distance to there is {dist[pf_pos]}')
        return dist[pf_pos]

def part1(input):
    rows = input.split('\n')
    columns = []
    for i in range(len(rows[0])):
        temp = ''
        for j in range(len(rows)):
            temp += rows[j][i]
        columns.append(temp)

    # print(f'rows = {rows}')
    # print(f'columns = {columns}')

    #columns[x][y] = x,y


    pos = (0,0)

    explored = [(0,0)]

    dist = {}

    prev = {}

    map = {}

    for i in range(len(columns)):
        for j in range(len(columns[0])):
            dist[(i,j)] = inf #x,y
            map[(i,j)] = int(columns[i][j])

    unexplored_dist = dist.copy()


    dist[(0,0)] = 0

    unexplored_dist.pop((0,0))
    # print(dist)


    repeat_dir = 0



    # x,y = pos

    # print(f'x = {x}, y = {y}')
    
    
    dist[(1,0)] = map[(1,0)]
    dist[(0,1)] = map[(0,1)]

    prev_dir_list = {}

    if dist[(1,0)] < dist[(0,1)]:
        pos = (1,0)
        explored.append((1,0))
    else:
        pos = (0,1)
        explored.append((0,1))

    prev_dir_list[(1,0)] = 'right'
    prev_dir_list[(0,1)] = 'down'

    prev[(1,0)] = (0,0)
    prev[(0,1)] = (0,0)
    repeat_dir = {}
    repeat_dir[(1,0)] = 1
    repeat_dir[(0,1)] = 1

    prev_dir_list[0,0] = None

    loop = 1
    while pos != (len(columns)-1, len(columns[0])-1):
        #print(f'In loop {loop} the position is {pos} and repeat_dir is at {repeat_dir[pos]}. Possible next choices are {next_pos(pos, ccw(prev_dir_list[pos]))}, {next_pos(pos, prev_dir_list[pos])}, or {next_pos(pos, ccw(prev_dir_list[pos]))}, with min distances of {check(pos, ccw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)}, {check(pos, prev_dir_list[pos], explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)}, and {check(pos, cw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)} respectively')
        print(f'In loop {loop} the pos is {pos} and repeat_dir is at {repeat_dir[pos]}')
        temp1 = 0
        temp2 = 0
        temp3 = 0
        if repeat_dir[pos] < 3:
            temp1 = check(pos, ccw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)
            temp2 = check(pos, prev_dir_list[pos], explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)
            temp3 = check(pos, cw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)
            # print(f'temp1 = {temp1}, temp2 = {temp2}, temp3 = {temp3}')
        
        elif repeat_dir[pos] == 3:
            #print('repeat dir is at 3')
            temp1 = check(pos, ccw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)
            temp2 = check(pos, cw(prev_dir_list[pos]), explored, dist, map, prev, columns, unexplored_dist, prev_dir_list)
        
        else:
            print(f'somehow repeat_dir is {repeat_dir[pos]} which is in fact greater than 3')
            print(f'At pos {pos}, repeat_dir is {repeat_dir[pos]} and at its prev position, {prev[pos]}, repeat_dir is {repeat_dir[prev[pos]]}')
            break
        
        min_temp = min(unexplored_dist.values())
        for key in unexplored_dist.keys():
            if unexplored_dist[key] == min_temp:
                pos = key
                break
            elif unexplored_dist[key] < min_temp:
                print('somehow you found a value lower than the minimum what ever happened to the WOP')
                break
        else:
            print('pos was not updated because somehow the min value of the list was not in the list :(')
        


        explored.append(pos)
        unexplored_dist.pop(pos)
        if prev_dir_list[pos] == prev_dir_list[prev[pos]]:
            repeat_dir[pos] = repeat_dir[prev[pos]] + 1
        else:
            repeat_dir[pos] = 1


        loop+=1
    print(f'In loop {loop} the position is {pos}')

    path_pos = (len(columns)-1, len(columns[0])-1)

    path = [path_pos]

    #print(prev)
    while path_pos != (0,0):
        path_pos = prev[path_pos]
        path.append(path_pos)
        #print(path)
        
    path.reverse()
    #
    print(path)

    # for key in dist.keys():
    #     if key not in explored:
    #         print(key)

    for item in path:
        if item != (0,0):
            print(f'dist to {item} from {prev[item]} = {dist[item]-dist[prev[item]]} and also {dist[item]-dist[prev[item]] == map[item]}')
    print(dist[(len(columns)-1, len(columns[0])-1)])





#part1(baby_input)
# part1(test_input)
part1(actual_input)


