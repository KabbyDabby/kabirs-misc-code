from aoc8input import test_input
from aoc8input import test_input2
from aoc8input import test_input3
from aoc8input import actual_input

def part1(input):
    rls = input.split('\n\n')[0]
    map = input.split('\n\n')[1]

    lines = map.split('\n')
    map_dict = {}
    for line in lines:
        map_dict[line[0:3] + 'L'] = line[7:10]
        map_dict[line[0:3] + 'R'] = line[12:15]

    #print(map_dict)
    #print(rls)
    #print(map)

    pos = 'AAA'
    z_reached = False
    steps = 0
    while z_reached == False:
        for i in range(len(rls)):
            pos = map_dict[pos+rls[i]]
            steps+=1
            if pos == 'ZZZ':
                z_reached = True
                break
    print(steps)

#part1(test_input)
#part1(test_input2)
#part1(actual_input)

def part2(input):
    rls = input.split('\n\n')[0]
    map = input.split('\n\n')[1]

    lines = map.split('\n')
    map_dict = {}
    possible_startings = []
    for line in lines:
        possible_startings.append(line[0:3])
        map_dict[line[0:3] + 'L'] = line[7:10]
        map_dict[line[0:3] + 'R'] = line[12:15]

    #print(map_dict)
    #print(rls)
    #print(map)

    poss = []
    z_reached_list = []
    for start_loc in possible_startings:
        if start_loc[2] == 'A':
            poss.append(start_loc)
            z_reached_list.append(False)


    print(poss)
    steps = 0
    while False in z_reached_list:
        for i in range(len(rls)):
            #print(poss)
            #print(z_reached_list)
            for j in range(len(poss)):
                poss[j] = map_dict[poss[j]+rls[i]]
                if poss[j][2] == 'Z':
                    z_reached_list[j] = True
                    print("Something Happened")
                    print(z_reached_list)
                else:
                    z_reached_list[j] = False
            steps+=1
            #print(steps)
            if False not in z_reached_list:
                break
    print(steps)

#part2(test_input3)
part2(actual_input)