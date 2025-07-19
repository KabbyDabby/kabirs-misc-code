from aoc14input import test_input,actual_input
from time import time




def part1(input):
    lines = input.split('\n')
    columns = []

    for i in range(len(lines[0])):
        columnx = ''
        for j in range(len(lines)):
            columnx += lines[j][i]
            five = 5
        
        columns.append(columnx)




    total = 0

    for column in columns:
        spheres = []
        cubes = []
        for i in range(len(column)):
            if column[i] == 'O':
                spheres.append(i)
            elif column[i] == '#':
                cubes.append(i)
        shifted = []

        # print(spheres)
        # print(cubes)



        for i in range(len(spheres)):
            cubes.sort()
            print(f'shifted = {shifted}')
            print(f'current sphere = {spheres[i]}')
            print(f'cubes = {cubes}')
            #print(spheres)
            for j in range(len(cubes)-1, -1, -1):
                if spheres[i] > cubes[j]:
                    shifted.append(cubes[j]+1)
                    cubes.append(cubes[j]+1)
                    break

            else:
                shifted.append(0)
                cubes.append(0)

        print(f'shifted = {shifted}')
        print(f'cubes = {cubes}')

        column_total = 0
        for sphere in shifted:
            column_total += len(column) - sphere

        total += column_total
        print(f'column total is {column_total} ')

    print(total)





def shift_up(spheres_total, cubes_unedited):
    cubes_total = []
    for blah in cubes_unedited:
        cubes_total.append(blah.copy())
    print(f'inner og cubes = {cubes_total}')
    shifted_total = []
    for k in range(len(spheres_total)):
        spheres = spheres_total[k]
        cubes = cubes_total[k]
        shifted = []
        for i in range(len(spheres)):
                cubes.sort()
                #print(f'shifted = {shifted}')
                #print(f'current sphere = {spheres[i]}')
                #print(f'cubes = {cubes}')
                #print(spheres)
                for j in range(len(cubes)-1, -1, -1):
                    if spheres[i] > cubes[j]:
                        shifted.append(cubes[j]+1)
                        cubes.append(cubes[j]+1)
                        break

                else:
                    shifted.append(0)
                    cubes.append(0)
        shifted_total.append(shifted)
    print(f"inner changed? cubes that shouldn't be returned = {cubes_total} vs {cubes_unedited}")
    return shifted_total

def shift_down(spheres_total, cubes_unedited, dir_len):
    cubes_total = []
    for blah in cubes_unedited:
        cubes_total.append(blah.copy())
    print(f'inner og cubes = {cubes_total}')
    shifted_total = []
    for k in range(len(spheres_total)):
        spheres = spheres_total[k]
        cubes = cubes_total[k]
        shifted = []
        for i in range(len(spheres)-1, -1, -1):
                cubes.sort()
                #print(f'shifted = {shifted}')
                #print(f'current sphere = {spheres[i]}')
                #print(f'cubes = {cubes}')
                #print(spheres)
                for j in range(len(cubes)):
                    if spheres[i] < cubes[j]:
                        shifted.append(cubes[j]-1)
                        cubes.append(cubes[j]-1)
                        break

                else:
                    shifted.append(dir_len-1)
                    cubes.append(dir_len-1)
        shifted_total.append(shifted)
    print(f"inner changed? cubes that shouldn't be returned = {cubes_total} vs {cubes_unedited}")
    return shifted_total


def invert(spheres, cubes, dir_len):
    new_spheres = []
    new_cubes = []

    for i in range(dir_len):
        new_spheres.append([])
        new_cubes.append([])

    for i in range(len(spheres)):
        for item in spheres[i]:
            new_spheres[item].append(i)
        for thing in cubes[i]:
            new_cubes[thing].append(i)

    for i in range(len(new_spheres)):
        new_spheres[i].sort()
        new_cubes[i].sort()
                       
    return (new_spheres,new_cubes)

def part2(input, n):
    rows = input.split('\n')
    columns = []

    for i in range(len(rows[0])):
        columnx = ''
        for j in range(len(rows)):
            columnx += rows[j][i]
            five = 5
        
        columns.append(columnx)

    column_length = len(columns[0])
    rows_length = len(rows[0])



    total = 0

    spheres = []

    cubes = []


    for column in columns:
        spheres_column = []
        cubes_column = []
        for i in range(len(column)):
            if column[i] == 'O':
                spheres_column.append(i)
            elif column[i] == '#':
                cubes_column.append(i)
        spheres.append(spheres_column)
        cubes.append(cubes_column)

    # print(spheres)
    # print(cubes)
    start_time = time()
    for _ in range(100000):
        print(f'true og spheres = {spheres}')
        print(f'true og cubes = {cubes}')
        spheres = shift_up(spheres, cubes) #shift up
        print(f'og spheres = {spheres}')
        print(f'og cubes = {cubes}')
        temp_inversion = invert(spheres, cubes, column_length) #inverts for left
        spheres = temp_inversion[0]
        cubes = temp_inversion[1]
        print(f'inverted spheres = {spheres}')
        print(f'inverted cubes = {cubes}')
        spheres = shift_up(spheres, cubes) #shift left
        print(f'og spheres = {spheres}')
        print(f'og cubes = {cubes}')
        temp_inversion = invert(spheres, cubes, rows_length) #inverts for down
        spheres = temp_inversion[0]
        cubes = temp_inversion[1]
        print(f'inverted spheres = {spheres}')
        print(f'inverted cubes = {cubes}')
        spheres = shift_down(spheres, cubes, column_length) #shift down
        print(f'og spheres = {spheres}')
        print(f'og cubes = {cubes}')
        temp_inversion = invert(spheres, cubes, column_length) #inverts for right
        spheres = temp_inversion[0]
        cubes = temp_inversion[1]
        print(f'inverted spheres = {spheres}')
        print(f'inverted cubes = {cubes}')
        spheres = shift_down(spheres, cubes, rows_length) #shift right
        print(f'og spheres = {spheres}')
        print(f'og cubes = {cubes}')
        temp_inversion = invert(spheres, cubes, rows_length) #inverts for up or final calc
        spheres = temp_inversion[0]
        cubes = temp_inversion[1]
        print(f'inverted spheres = {spheres}')
        print(f'inverted cubes = {cubes}')
    

    print(time() - start_time)






    total = 0
    for i in range(len(spheres)):
        column_total = 0
        for sphere in spheres[i]:
            column_total += column_length - sphere
        total += column_total
        #print('column total = ')

    print(total)

    



        



#part1(test_input)
#part1(actual_input)#105003

#part2(test_input, 1000000000)
part2(actual_input, 1000000000)#93781