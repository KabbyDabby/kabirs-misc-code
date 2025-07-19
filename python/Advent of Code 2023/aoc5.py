from aoc5input import test_string
from aoc5input import actual_input
#import re

def part1(input):
    print(input)
    steps = input.split('\n\n')
    seeds = steps[0] #s2s, s2f, f2w, w2l, l2t, t2h, h2l
    steps.pop(0)
    seeds = seeds.split(':')[1].split(' ')
    seeds.remove('')
    seeds_dict = {}
    for i in range(len(seeds)):
        seeds[i] = int (seeds[i])
    
    for seed in seeds:
        seeds_dict[seed] = seed
    print(seeds)
    print(seeds_dict)

    #print(seeds)
    for step in steps:
        print(step)
        lines = step.split('\n')
        lines.pop(0)
        big_convo = {}
        xlist = []
        for line in lines:
            x = line.split(' ')
            print(x)
            conversion = {}
            #print(x)
            for c in range(len(x)):
                x[c] = int (x[c])
            #print(x)
            #for j in range(x[2]):#delete
            #    conversion[x[1]+j] = x[0]+j

            xlist.append(x)
            #for key in conversion.keys():
            #    big_convo[key] = conversion[key]
        #print('conversion:')
        #print(big_convo)
        print('current seeds_dict:')
        print(seeds_dict)
        for seed in seeds:
            if check(seed, seeds_dict, xlist) != -1:
                seeds_dict[seed] = check(seed, seeds_dict, xlist)
        

        #print('after conversion keys:')
        #print(big_convo)
        #print('after seeds_dict:')
        #print(seeds_dict)   
    min_final = seeds_dict[seeds[0]]
    for seed in seeds:
        if seeds_dict[seed] < min_final:
            min_final = seeds_dict[seed]
    print(min_final)
        

def check(seed, seeds_dict, xlist):
    for x in xlist:
        if seeds_dict[seed] >= x[1] and seeds_dict[seed]<= x[1]+x[2]-1:
                    return x[0] + seeds_dict[seed] - x[1]
    
    else:
         return -1


def part2(input,number):
    #print(input)
    steps = input.split('\n\n')
    seeds = steps[0]
    seeds = seeds.split(':')[1].split(' ')
    seeds.remove('')
    #print(seeds)
    for k in range(len(seeds)):
        seeds[k] = int (seeds[k])
    steps.pop(0)
    steps.reverse()
    #print(steps)
    output_number = number
    for step in steps:
        lines = step.split('\n')
        lines.pop(0)
        for line in lines:
            x = line.split(' ')
            #print(x)
            for i in range(len(x)):
                x[i] = int (x[i])
            if output_number >= x[0] and output_number < x[0] + x[2]:
                 output_number = x[1] + output_number - x[0]

    #print(seeds)
    #print(len(seeds))
    for j in range(len(seeds)):
        if j % 2 == 0:
            if output_number >= seeds[j] and output_number < seeds[j]+ seeds[j+1]:
                print(output_number)
                return number
    print(-1)
    return -1
                   
def part2redo(input, numberthing):      
    steps = input.split('\n\n')
    seeds = steps[0]
    steps.pop(0)

    currentnum = numberthing

    seeds = seeds.split(':')[1].split(' ')
    seeds.remove('')

    for a in range(len(seeds)):
        seeds[a] = int (seeds[a])
    
    steps.reverse()
    
    for step in steps:
        lines = step.split('\n')

        lines.pop(0)

        for line in lines:
            x = line.split(' ')

            for b in range(len(x)):
                x[b] = int (x[b])

            if currentnum >= x[0] and currentnum< x[0] + x[2]:
                currentnum = x[1] + (currentnum-x[0]) 


    for i in range(len(seeds)):
        if i % 2 == 0:
            if currentnum >= seeds[i] and currentnum<(seeds[i] + seeds[i+1]):
                print(currentnum)
                return currentnum
    print(-1)
    return -1
            
              

#ahahahaaahahahah why not working ljljlkjlkjkjkjkjkjijijijijijijijijijijijiiiij
#part1(test_string)
#part1(actual_input)
answer = 0# 50716416

part2redo(actual_input, 641411)
part2redo(actual_input, 50716416)
