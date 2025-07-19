from aoc1input import test_string
from aoc1input import actual_input

def part1(input):
    print('Hello World!')

    lines =  input.split('\n')


    total = 0
    for line in lines:
        numbers = [c for c in line if c.isnumeric()]

        if len(numbers) != 0:
            total+= int (numbers[0]+numbers[-1])

    print(total)


def numberChecker(c, line):
    if line[c].isnumeric():
        print("isNumeric proc or w/e")
        return str(line[c])
    if line[c:c+3] == "one" and c+2<len(line):
        return '1'
    if line[c:c+3] == "two" and c+2<len(line):
        return '2'
    if line[c:c+5] == "three" and c+4<len(line):
        return '3'
    if line[c:c+4] == "four" and c+3<len(line):
        return '4'
    if line[c:c+4] == "five" and c+3<len(line):
        return '5'
    if line[c:c+3] == "six" and c+2<len(line):
        return '6'
    if line[c:c+5] == "seven" and c+4<len(line):
        return '7'
    if line[c:c+5] == "eight" and c+4<len(line):
        return '8'
    if line[c:c+4] == "nine" and c+3<len(line):
        return '9'
    
    return '-1'

def part2(input):
    print('Hello World!')

    lines = [x for x in input.split('\n')]

    total = 0

    for line in lines:
        print(line)
        numbers = []
        for i in range(len(line)):
            print(line[i])
            if numberChecker(i, line) != '-1':
                numbers.append(numberChecker(i,line))
            
        if len(numbers) != 0:
                print(numbers)
                total+= int (numbers[0]+numbers[-1])
        
    print(total)




#part1(test_string)

part2(test_string) #281

part2(actual_input) #55686
