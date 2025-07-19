from aoc9input import test_input
from aoc9input import actual_input

def last_elements_equal(list):
    #print(list)
    thing = list[0]
    for i in range(len(list)):
        if list[i] != thing:
            return False
    
    return True

def part1(input):
    lines = input.split('\n')
    total = 0
    for line in lines:
        numbers = line.split(' ')
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
        list_thing = [numbers]
        temp_list = []
        #print(list_thing[-1])
        while not last_elements_equal(list_thing[-1]):
            
            for i in range(1, len(list_thing[-1])):
                temp_list.append(list_thing[-1][i]-list_thing[-1][i-1])
            #print(temp_list)
            list_thing.append(temp_list)
            temp_list = []
            #print(list_thing)
        #print(list_thing)
        thingie = 0
        #print(len(list_thing))
        ahah = []

        for i in range(len(list_thing)):
            ahah.append(i)
        
        ahah.reverse()
        print(ahah)
        print('ahah^^^')
        for i in ahah:
            #print(i)
            print(list_thing[i])
            thingie += list_thing[i][-1]
            print(thingie)
            #print("test")
        #print(list_thing)
        #print(thingie)
        total+=thingie
    print(total)


    print("AHAHAHAH")


def part2(input):
    lines = input.split('\n')
    total = 0
    for line in lines:
        numbers = line.split(' ')
        for i in range(len(numbers)):
            numbers[i] = int(numbers[i])
        list_thing = [numbers]
        temp_list = []
        #print(list_thing[-1])
        while not last_elements_equal(list_thing[-1]):
            
            for i in range(1, len(list_thing[-1])):
                temp_list.append(list_thing[-1][i]-list_thing[-1][i-1])
            #print(temp_list)
            list_thing.append(temp_list)
            temp_list = []
            #print(list_thing)
        #print(list_thing)
        thingie = 0
        #print(len(list_thing))
        ahah = []

        for i in range(len(list_thing)):
            ahah.append(i)
        
        ahah.reverse()
        print(ahah)
        print('ahah^^^')
        for i in ahah:
            #print(i)
            print(list_thing[i])
            thingie = list_thing[i][0] - thingie
            print(thingie)
            #print("test")
        #print(list_thing)
        #print(thingie)
        print(thingie)
        print('final thingie^^^')
        total+=thingie
    print(total)


    print("AHAHAHAH")

#part1(test_input)
#part1(actual_input)

#part2(test_input)
part2(actual_input)
