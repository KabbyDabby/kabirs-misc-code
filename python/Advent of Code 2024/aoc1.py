from aoc1input import test_input, actual_input
import heapq as hq

def part1(input):
    lines = input.split('\n')
    
    l1,l2 = [],[]
    hq.heapify(l1)
    hq.heapify(l2)

    for line in lines:
        nums = [int(c) for c in line.split() if c!='']

        hq.heappush(l1, nums[0])
        hq.heappush(l2, nums[1])

    ret = 0
    while l1:
        ret+=abs(hq.heappop(l1)-hq.heappop(l2))
    
    return ret


def part2(input):
    lines = input.split('\n')
    l1,l2 = [],[]

    for line in lines:
        nums = [int(c) for c in line.split() if c != '']

        l1.append(nums[0])
        l2.append(nums[1])


    counts = {}
    for num in l2:
        counts[num] = counts.get(num,0)+1
    
    ret = 0

    for num in l1:
        ret+=num*counts.get(num,0)
    
    return ret

    

# print(part1(actual_input))
print(part2(actual_input))