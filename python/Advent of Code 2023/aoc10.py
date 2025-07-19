from aoc10input import test_input1
from aoc10input import test_input2
from aoc10input import test_input3
from aoc10input import test_input4
from aoc10input import test_input5
from aoc10input import actual_input
import math

def s_locator(lines):
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == 'S':
                return (i, j)


def decide_next_dir(past_dir, curr_pos):
    #up, down, left, right
    if curr_pos == '|' or curr_pos == '-':
        return past_dir
    elif curr_pos == 'L':
        if past_dir == 'down':
            return 'right'
        elif past_dir == 'left':
            return 'up'
        else:
            print('AHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA1')
    elif curr_pos == 'J':
        if past_dir == 'down':
            return 'left'
        elif past_dir == 'right':
            return 'up'
        else:
            print('AHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA2')
    elif curr_pos == '7':
        if past_dir == 'up':
            return 'left'
        elif past_dir == 'right':
            return 'down'
        else:
            print('AHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA3')
    
    elif curr_pos == 'F':
        if past_dir == 'up':
            return 'right'
        elif past_dir == 'left':
            return 'down'
        else:
            print('AHAHAHAHAHAHAHAHAHAHAHAHAHAHAHA4')
    else:
        print("AHAHAHAHAHAHAHAHAHAHAHAH5")

    

def part1(input):
    lines = input.split('\n') #lines[row][column]
    s_loc = s_locator(lines) #y, x (row, column)

    #print(s_loc)
    #print(lines[s_loc[0]][s_loc[1]])
    up = ''
    down = ''
    left = ''
    right = ''
    if s_loc[0] != 0:
        up = lines[s_loc[0]-1][s_loc[1]]
    if s_loc[0] != len(lines) - 1:
        down = lines[s_loc[0]+1][s_loc[1]]
    if s_loc[1] != 0:
        left = lines[s_loc[0]][s_loc[1]-1]
    if s_loc[1] != len(lines) - 1:
        right = lines[s_loc[0]][s_loc[1]+1]
    
    starters = []

    if up == '|' or up == '7' or up == 'F':
        starters.append('up')
    if down == '|' or down == 'L' or down == 'J':
        starters.append('down')
    if left == '-' or left == 'L' or left == 'F':
        starters.append('left')
    if right == '-' or right == 'J' or right == '7':
        starters.append('right')
    print(starters)

    if len(starters) != 2:
        print('AHAHAHAHAHHA')

    current_pos = 'S'

    current_loc = s_loc

    current_dir = starters[0]

    step = 0

    step+=1
    if current_dir == 'right':
        current_loc = (current_loc[0], current_loc[1]+1) #y, x
    elif current_dir == 'left':
        current_loc = (current_loc[0], current_loc[1]-1) #y, x
    elif current_dir == 'up':
        current_loc = (current_loc[0]-1, current_loc[1]) #y, x
    elif current_dir == 'down':
        current_loc = (current_loc[0]+1, current_loc[1]) #y, x
    current_pos = lines[current_loc[0]][current_loc[1]]

    print(step)
    print(current_loc)
    print(current_pos)
    print(current_dir)
    print('fyi first')


    while current_pos != 'S':
        step+=1
        current_dir = decide_next_dir(current_dir, current_pos)
        if current_dir == 'right':
            current_loc = (current_loc[0], current_loc[1]+1) #y, x
        elif current_dir == 'left':
            current_loc = (current_loc[0], current_loc[1]-1) #y, x
        elif current_dir == 'up':
            current_loc = (current_loc[0]-1, current_loc[1]) #y, x
        elif current_dir == 'down':
            current_loc = (current_loc[0]+1, current_loc[1]) #y, x
        current_pos = lines[current_loc[0]][current_loc[1]]
        print(step)
        print(current_loc)
        print(current_pos)

    print(step)

    print(math.floor(step/2))


def shoelace(list):
    first_sum = 0
    second_sum = 0
    for i in range(len(list)-1, -1, -1):
        first_sum += list[i][0]*list[i-1][1]
        second_sum += list[i][1]*list[i-1][0]
    return abs((first_sum-second_sum)/2)

def part2(input):
    lines = input.split('\n') #lines[row][column]
    s_loc = s_locator(lines) #y, x (row, column)

    #print(s_loc)
    #print(lines[s_loc[0]][s_loc[1]])
    up = ''
    down = ''
    left = ''
    right = ''
    if s_loc[0] != 0:
        up = lines[s_loc[0]-1][s_loc[1]]
    if s_loc[0] != len(lines) - 1:
        down = lines[s_loc[0]+1][s_loc[1]]
    if s_loc[1] != 0:
        left = lines[s_loc[0]][s_loc[1]-1]
    if s_loc[1] != len(lines) - 1:
        right = lines[s_loc[0]][s_loc[1]+1]
    
    starters = []

    if up == '|' or up == '7' or up == 'F':
        starters.append('up')
    if down == '|' or down == 'L' or down == 'J':
        starters.append('down')
    if left == '-' or left == 'L' or left == 'F':
        starters.append('left')
    if right == '-' or right == 'J' or right == '7':
        starters.append('right')
    print(starters)

    if len(starters) != 2:
        print('AHAHAHAHAHHA')


    boundary_list = []

    current_pos = 'S'

    current_loc = s_loc

    current_dir = starters[0]

    step = 0

    boundary_list.append(current_loc)

    step+=1
    if current_dir == 'right':
        current_loc = (current_loc[0], current_loc[1]+1) #y, x
    elif current_dir == 'left':
        current_loc = (current_loc[0], current_loc[1]-1) #y, x
    elif current_dir == 'up':
        current_loc = (current_loc[0]-1, current_loc[1]) #y, x
    elif current_dir == 'down':
        current_loc = (current_loc[0]+1, current_loc[1]) #y, x
    current_pos = lines[current_loc[0]][current_loc[1]]


    print(step)
    print(current_loc)
    print(current_pos)
    print(current_dir)
    print('fyi first')


    while current_pos != 'S':
        boundary_list.append(current_loc)
        step+=1
        current_dir = decide_next_dir(current_dir, current_pos)
        if current_dir == 'right':
            current_loc = (current_loc[0], current_loc[1]+1) #y, x
        elif current_dir == 'left':
            current_loc = (current_loc[0], current_loc[1]-1) #y, x
        elif current_dir == 'up':
            current_loc = (current_loc[0]-1, current_loc[1]) #y, x
        elif current_dir == 'down':
            current_loc = (current_loc[0]+1, current_loc[1]) #y, x
        current_pos = lines[current_loc[0]][current_loc[1]]
        print(step)
        print(current_loc)
        print(current_pos)

    area = shoelace(boundary_list)
    #step = boundary
    #A = B/2 + I -1
    #I = A-B/2+1

    print(area-(step/2)+1)





    


#part1(test_input1)    
#part1(test_input2)
#part1(actual_input)

#part2(test_input3)    
#part2(test_input4)
#part2(test_input5)
part2(actual_input)