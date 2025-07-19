from aoc11input import test_input
from aoc11input import actual_input

def part1(input): #also part 2 lol
    lines = input.split('\n')
    empty_rows = []

    for i in range(len(lines)):
        if '#' not in lines[i]:
            empty_rows.append(i)

    print(empty_rows)


    columns = []
    empty_columns = []
    for i in range(len(lines[0])):
        columns.append('')
        for j in range(len(lines)):
            columns[i] += lines[j][i]

    for i in range(len(columns)):
        if '#' not in columns[i]:
            empty_columns.append(i)

    print(empty_columns)

    galaxies = []
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                galaxies.append((i,j)) #rows, columns
    
    print(galaxies)

    total = 0


    for galaxy1 in galaxies:
        for galaxy2 in galaxies:
            x = [galaxy1[1], galaxy2[1]]
            x.sort()
            y = [galaxy1[0], galaxy2[0]]
            y.sort()
            output = y[1] - y[0] + x[1] - x[0]
            for column in empty_columns:
                if x[0] < column and x[1] > column:
                    output +=999999
            for row in empty_rows:
                if y[0] < row and y[1] > row:
                    output+=999999# this and above "output +=" row are what you change to make it part 1 or part 2
                    #part 1 += 1, part 2 += 999999
            total+=output
    total /= 2
    print(total)




#part1(test_input)
part1(actual_input)