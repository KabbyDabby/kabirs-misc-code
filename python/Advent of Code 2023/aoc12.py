from aoc12input import test_input
from aoc12input import actual_input

def part1(input):
    lines = input.split('\n')

    total = 0

    for line in lines:
        temp = line.split(' ')
        nums = temp[1].split(',')
        springs = temp[0].split('.')
        while '' in springs:
            springs.remove('')
        print(springs)
        print(nums)

        if len(springs) == len(nums):
            total+=1
            continue
        else:
            print('boop')

#IM COMING BACK IDRC AHAHAHAHAHAH




part1(test_input)