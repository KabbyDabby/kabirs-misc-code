from aoc18input import test_input

def part1(input):
    lines = input.split('\n')
    boundary = 1
    lattices = [(0,0)]
    last_hor = ''
    last_vert = ''
    for line in lines:
        last_lattice = lattices[-1]
        dir, num, color = [x for x in line.split(' ') if x != '']
        num = int(num)
        boundary+=num-1
        print(f'dir = {dir}, num = {num}, color = {color}, last_lattice = {last_lattice}')
        if dir == 'R':
            if last_hor != 'R':
                lattices.append((last_lattice[0]+num+1, last_lattice[1]))
            else:
                lattices.append((last_lattice[0]+num, last_lattice[1]))
            last_hor = 'R'

        elif dir == 'U':
            if last_vert != 'U':
                lattices.append((last_lattice[0], last_lattice[1]+num+1))
            else:
                lattices.append((last_lattice[0], last_lattice[1]+num))
            last_vert = 'U'

        elif dir == 'L':
            if last_hor != 'L':
                lattices.append((last_lattice[0]-num-1, last_lattice[1]))
            else:
                lattices.append((last_lattice[0]-num, last_lattice[1]))
            last_hor = 'L'

        elif dir == 'D':
            if last_vert != 'D':
                lattices.append((last_lattice[0], last_lattice[1]-num-1))
            else:
                lattices.append((last_lattice[0], last_lattice[1]-num))
            last_vert = 'D'

        else:
            print('fix ur code')
            break
    

    print(lattices)
    sum1 = 0
    sum2 = 0
    for i in range(1, len(lattices)):
        sum1+=lattices[i][1]*lattices[i-1][0]
        sum2+=lattices[i][0]*lattices[i-1][1]
    
    print(abs(sum1-sum2)/2)

part1(test_input)