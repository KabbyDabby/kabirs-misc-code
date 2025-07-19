from aoc3input import test_string
from aoc3input import actual_input

def ispart(num, gears, lines):
    min_line = 0
    max_line = 0
    min_ind = 0
    max_ind = 0
    if int (num[-7:-4]) > 0:
        min_line = int (num[-7:-4]) - 1
    else:
        min_line = 0
    
    if int(num[-7:-4]) < len(lines) - 1:
        max_line = int(num[-7:-4]) + 1
    else:
        max_line = len(lines) - 1
    
    if int(num[-4:-1]) > 0:
        min_ind = int(num[-4:-1]) - 1
    else: 
        min_ind = 0
    
    if int(num[-4:-1]) + int(num[-1]) - 1 < len(lines[int(num[-7:-4])]) - 1:
        max_ind =  int(num[-4:-1]) + int(num[-1])
    else:
        max_ind = len(lines[int(num[-7:-4])]) - 1

    for a in range(min_line, max_line+1):
        for b in range(min_ind, max_ind+1):
            if str(a).zfill(3) + str(b).zfill(3) in gears:
                print (str(a)+str(b))
                return True
    return False

def real_gears(num, gears, lines):
    min_line = 0
    max_line = 0
    min_ind = 0
    max_ind = 0
    if int (num[-7:-4]) > 0:
        min_line = int (num[-7:-4]) - 1
    else:
        min_line = 0
    
    if int(num[-7:-4]) < len(lines) - 1:
        max_line = int(num[-7:-4]) + 1
    else:
        max_line = len(lines) - 1
    
    if int(num[-4:-1]) > 0:
        min_ind = int(num[-4:-1]) - 1
    else: 
        min_ind = 0
    
    if int(num[-4:-1]) + int(num[-1]) - 1 < len(lines[int(num[-7:-4])]) - 1:
        max_ind =  int(num[-4:-1]) + int(num[-1])
    else:
        max_ind = len(lines[int(num[-7:-4])]) - 1


    new_gears = []
    for gear in gears:
        for a in range(min_line, max_line+1):
            for b in range(min_ind, max_ind+1):
                if str(a).zfill(3) + str(b).zfill(3) == gear[:6]:
                    print (str(a)+str(b))
                    if gear[-1] == '0':
                        print('end = 0 before: ' + gear)
                        gear = gear[:6] + num[:-7].zfill(3) + gear[-4:-1] + '1'
                        print('end = 0 after: ' + gear)
                    elif gear[-1] == '1':
                        print('end = 1 before: ' + gear)
                        gear = gear[:9] + num[:-7].zfill(3) + '2'
                        print('end = 1 before: ' + gear)
                    else:
                        print("end = else before (shouldn't proc): " + gear)
                        gear = gear[:9] + num[:-7].zfill(3) + '3'
                        print("end = else before (shouldn't proc): " + gear)
                    break
            else:
                continue
            break
        new_gears.append(gear)

    return new_gears
def part1(input):
    lines = [x for x in input.split('\n')]
    j = 0
    numbers = []
    symbols = []
    while j<len(lines):
        i=0
        #print(lines[j])
        while i<len(lines[j]):
            if lines[j][i].isdecimal():
                c=i
                number = ''
                #print(lines[j][i])
                while c<len(lines[j]) and lines[j][c].isdecimal():
                    print('c = ' + str(c) + '| len(lines[j] = )' + str(len(lines[j])))
                    #print('c = ' + str(c) + ' and len(lines[j]) = ' + str(len(lines[j])))
                    number += lines[j][c]
                    c+=1
                print(number)
                numbers.append(number +  str(j).zfill(3) + str(i).zfill(3) + str(len(number))) #number, line, starting index, length
                i+=int (numbers[-1][-1])
            elif lines[j][i] != '.': 
                symbols.append(str(j).zfill(3)+str(i).zfill(3)) #line, index
                i+=1
            else:
                i+=1
            
        j+=1
    print(numbers)
    print(symbols)
    total = 0
    for num in numbers:
         if ispart(num, symbols, lines):
            total += int(num[:len(num)-7])

    print(total)

def part2(input):
    lines = [x for x in input.split('\n')]
    j = 0
    numbers = []
    gears = []
    while j<len(lines):
        i=0
        #print(lines[j])
        while i<len(lines[j]):
            if lines[j][i].isdecimal():
                c=i
                number = ''
                #print(lines[j][i])
                while c<len(lines[j]) and lines[j][c].isdecimal():
                    print('c = ' + str(c) + '| len(lines[j]) = ' + str(len(lines[j])))
                    #print('c = ' + str(c) + ' and len(lines[j]) = ' + str(len(lines[j])))
                    number += lines[j][c]
                    c+=1
                print(number)
                numbers.append(number +  str(j).zfill(3) + str(i).zfill(3) + str(len(number))) #number, line, starting index, length
                i+=int (numbers[-1][-1])
            elif lines[j][i] == '*': 
                gears.append(str(j).zfill(3)+str(i).zfill(3)+'0000000') #line, index, num1, num2, # of adjacent numbers
                i+=1
            else:
                i+=1
            
        j+=1
    print(numbers)
    print(gears)
    for num in numbers:
        gears = real_gears(num, gears, lines)
    
    gear_ratio = 0
    for gear in gears:
        if gear[-1] == '2':
            gear_ratio += int(gear[-7:-4]) * int(gear[-4:-1])

    print(gears)
    print(gear_ratio)
    


#part1(test_string)

#part1(actual_input)

part2(test_string)

part2(actual_input)