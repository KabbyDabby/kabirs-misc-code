from aoc2input import test_input,actual_input

def part1(input):
    reports = input.split('\n')
    ret = 0
    count = 0
    print(reports)
    for report in reports:
        levels = [int(num) for num in report.split()]
        
        diffs = [levels[i]-levels[i-1] for i in range(1,len(levels))]
        print(diffs)
        if abs(diffs[0]) < 1 or abs(diffs[0]) > 3:
            continue
        count+=1
        for i in range(1, len(diffs)):
            if abs(diffs[i]) < 1 or abs(diffs[i]) > 3 or diffs[i]*diffs[i-1]<0:
                break
        else: 
            ret+=1
    print(len(reports))
    print(count)
    return ret

def part2(input):
    reports = input.split('\n')
    ret = 0
    # print(reports)
    for report in reports:
        # print("ret:", ret)
        levels = [int(num) for num in report.split()]
        # print("levels:", levels)
        diffs = [levels[i]-levels[i-1] for i in range(1,len(levels))]
        # print("diffs:", diffs)
        if abs(diffs[0]) < 1 or abs(diffs[0]) > 3:
            # print("ret:", ret)
            print("levels:", levels)
            print("diffs:", diffs)
            nums = levels[1:]
            # print("nums:",nums)
            print("check(nums):",check(nums))
            ret+=check(nums)
            continue
        for i in range(1, len(diffs)):
            if abs(diffs[i]) < 1 or abs(diffs[i]) > 3 or diffs[i]*diffs[i-1]<0:
                # print("ret:", ret)
                print("levels:", levels)
                print("diffs:", diffs)
                nums = levels[:i]
                nums.extend(levels[i+1:])
                # print("nums:",nums)
                print("check(nums):",check(nums))
                ret+=check(nums)
                break
        else: 
            ret+=1
    return ret

def check(levels):
    diffs = [levels[i]-levels[i-1] for i in range(1,len(levels))]
    # print(diffs)
    if abs(diffs[0]) < 1 or abs(diffs[0]) > 3:
        return False
    for i in range(1, len(diffs)):
        if abs(diffs[i]) < 1 or abs(diffs[i]) > 3 or diffs[i]*diffs[i-1]<0:
            return False
    else: 
        return True

print("ans:", part2(actual_input))