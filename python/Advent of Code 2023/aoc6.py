from aoc6input import test_input
from aoc6input import actual_input
import math

def part1(input):
    lines = input.split('\n')
    nums = []
    for line in lines:
        x = line.split(' ')
        while '' in x:
            x.remove('')
        x.pop(0)
        for i in range(len(x)):
            x[i] = int (x[i])
        #print(x)
        nums.append(x)
        
    #print(nums)
    time = nums[0]
    distance = nums[1]
    final = 1
    for j in range(len(time)):
        goal = distance[j]
        t = time[j]

        ans = []
        
        ans.append((t-math.sqrt(t**2-4*goal))/2)
        ans.append((t+math.sqrt(t**2-4*goal))/2)

        ans[0] = math.floor(ans[0]+1)
        ans[1] = math.ceil(ans[1]-1)

        final *= (ans[1]-ans[0]+1)
        #-xtime+ x^2 + goal
        #(time+-sqrt(time-4goal)/2)

    print(final)

def part2(input):
    lines = input.split('\n')
    nums = []
    for line in lines:
        x = line.split(' ')
        while '' in x:
            x.remove('')
        x.pop(0)
        for i in range(len(x)):
            x[i] = int (x[i])
        #print(x)
        nums.append(x)
        
    #print(nums)
    time = nums[0]
    print(time)
    distance = nums[1]
    print(distance)
    act_time = ''
    act_dist = ''
    for i in range(len(time)):
        act_time = int (str(act_time)+str(time[i]))
        act_dist = int (str(act_dist)+str(distance[i]))

    print(act_time)
    print(act_dist)

    ans = []
    
    ans.append((act_time-math.sqrt(act_time**2-4*act_dist))/2)
    ans.append((act_time+math.sqrt(act_time**2-4*act_dist))/2)

    ans[0] = math.floor(ans[0]+1)
    ans[1] = math.ceil(ans[1]-1)

    final = (ans[1]-ans[0]+1)
    #-xtime+ x^2 + goal
    #(time+-sqrt(time-4goal)/2)

    print(final)

#part2(test_input)
part2(actual_input)