from aoc7input import test_input, actual_input


def part1(input):
    lines = input.strip().split("\n")
    ret = 0
    for line in lines:
        # print(line)
        answer, numbers = line.strip().split(": ")
        answer = int(answer)
        numbers = [int(n) for n in numbers.split(" ")]
        for n in range(2 ** (len(numbers) - 1)):
            running = numbers[0]
            for i in range(1, len(numbers)):
                if n & (1 << (i - 1)):
                    running *= numbers[i]
                else:
                    running += numbers[i]
                if running > answer:
                    break
            if running == answer:
                print(answer)
                ret += answer
                break
    return ret


# print(f"test: {part1(test_input)}")
# print(f"actual: {part1(actual_input)}")


def part2(input):
    lines = input.strip().split("\n")
    ret = 0
    for line in lines:
        # print(line)
        answer, numbers = line.strip().split(": ")
        answer = int(answer)
        numbers = [int(n) for n in numbers.split(" ")]
        for n in range(3 ** (len(numbers) - 1)):
            running = numbers[0]
            for i in range(1, len(numbers)):
                if n % 3 == 0:
                    running *= numbers[i]
                elif n % 3 == 1:
                    running += numbers[i]
                else:
                    running = int(str(running) + str(numbers[i]))

                n //= 3
                if running > answer:
                    break
            if running == answer:
                print(answer)
                ret += answer
                break
    return ret


print(f"test: {part2(test_input)}")
print(f"actual: {part2(actual_input)}")
