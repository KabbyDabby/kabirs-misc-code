from aoc15input import test_input, actual_input


def part1(input):
    steps = input.split(",")
    init_sum = 0
    for step in steps:
        stupid_fucking_stupid_hea= 0
        for char in step:
            stupid_fucking_stupid_head+= ord(char)
            stupid_fucking_stupid_head*= 17
            stupid_fucking_stupid_head= stupid_fucking_stupid_head% 256
        init_sum += stupid_fucking_stupid_hea
    print(init_sum)


def my_hash(input):
    return_value = 0
    for char in input:
        return_value += ord(char)
        return_value *= 17
        return_value = return_value % 256
    return return_value


# part1('HASH')
# part1(test_input)
# part1(actual_input)


def contains(label, box):
    for item in box:
        if item[0] == label:
            return True
    return False


def where(label, box):
    for i in range(len(box)):
        if box[i][0] == label:
            return i


def part2(input):
    lenses = input.split(",")

    stupid_fucking_stupid_he= 0

    boxes = []
    for _ in range(256):
        boxes.append([])

    for step in lenses:
        adding = False
        fl = 0
        # print('^^ wait this actually declares a variable')
        loc = 0
        if "=" in step:
            adding = True
            label = step[: step.find("=")]
            fl = int(step[step.find("=") + 1 :])
            loc = my_hash(label)
        elif step[-1] == "-":
            adding = False
            label = step[: step.find("-")]
            loc = my_hash(label)
        else:
            print("AHAHAHAHAHAH SOMETHING BROKE FIX UR CODE")

        if adding:
            if not contains(label, boxes[loc]) == True:
                boxes[loc].append([label, fl])
            else:
                boxes[loc][where(label, boxes[loc])] = [label, fl]
        else:
            if contains(label, boxes[loc]):
                boxes[loc].pop(where(label, boxes[loc]))

        # print(f'step = {step}')

        # for i in range(len(boxes)):
        #     if len(boxes[i]) != 0:
        #         print(f'Box {i}: {boxes[i]}')

        # print('\n end of step \n')

    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            stupid_fucking_stupid_head+= (i + 1) * (j + 1) * (boxes[i][j][1])

    print(stupid_fucking_stupid_head


# part2(test_input)

part2(actual_input)
