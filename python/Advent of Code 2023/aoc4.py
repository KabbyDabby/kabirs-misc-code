from aoc4input import test_string
from aoc4input import actual_input

def part1(input):
    lines = input.split('\n')
    print(lines)
    total = 0
    for line in lines:
        parts = line.split('|')
        y = parts[0].find(":")
        win_string = parts[0][y+1:].split(' ')
        my_string = parts[1].split(' ')
        while '' in win_string:
            win_string.remove('')
        while '' in my_string:
            my_string.remove('')
        
        win_nums = []
        for num in win_string:
            win_nums.append(int (num))
        
        my_nums = []
        for num in my_string:
            my_nums.append(int (num))
        
        count = 0
        for num in my_nums:
            if num in win_nums:
                count+=1
        if count>0:
            total+=2**(count-1)
            print(count)
    print(total)

def part2(input):
    lines = input.split('\n')
    card_list =[]
    total = 0
    for i in range(len(lines)):
        card_list.append(1)


    for line in lines:
        parts = line.split('|')
        y = parts[0].find(":")
        game_number = 0
        if parts[0][y-3].isdecimal():
            game_number = int (parts[0][y-3:y])
        elif parts[0][y-2].isdecimal():
            game_number = int (parts[0][y-2:y])
        else:
            game_number = int (parts[0][y-1])
        win_string = parts[0][y+1:].split(' ')
        my_string = parts[1].split(' ')
        while '' in win_string:
            win_string.remove('')
        while '' in my_string:
            my_string.remove('')
        
        win_nums = []
        for num in win_string:
            win_nums.append(int (num))
        
        my_nums = []
        for num in my_string:
            my_nums.append(int (num))

        print('game number = ' + str(game_number))
        print(win_nums)
        print(my_nums)
        count = 0
        for num in my_nums:
            if num in win_nums:
                count+=1

        for z in range(card_list[game_number-1]):
            for j in range(count):
                card_list[game_number+j]+= 1
        print(count)
        print(card_list)

    for k in range(len(card_list)):
        total+=card_list[k]
    print(total)


        


#part1(test_string)
#part1(actual_input)
part2(test_string)

part2(actual_input)