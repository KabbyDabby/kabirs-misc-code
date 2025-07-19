from aoc2input import test_input, actual_input


def part1(input):
    nums = [int(n) for n in input.split(",")]

    nums[1] = 12
    nums[2] = 2

    for i in range(0, len(nums), 4):
        assert nums[i] == 1 or nums[i] == 2 or nums[i] == 99, "Bruh"
        if nums[i] == 99:
            return nums

        print(i, nums[i])
        print(i + 1, nums[i + 1], nums[nums[i + 1]])
        print(i + 2, nums[i + 2], nums[nums[i + 2]])
        print(i + 3, nums[i + 3], nums[nums[i + 3]])
        print(nums)
        if nums[i] == 1:
            nums[nums[i + 3]] = nums[nums[i + 1]] + nums[nums[i + 2]]

        else:
            assert nums[i] == 2, f"{(i, nums[i])}"
            nums[nums[i + 3]] = nums[nums[i + 1]] * nums[nums[i + 2]]
        # else:
        #     return nums[0] #ig?

    else:
        print("idk")


def part2(input):
    for m in range(100):
        for n in range(100):
            nums = [int(n) for n in input.split(",")]
            nums[1] = m
            nums[2] = n
            for i in range(0, len(nums), 4):
                try:
                    assert (
                        nums[i] == 1 or nums[i] == 2 or nums[i] == 99
                    ), f"{(i,nums[i],nums)}"
                except:
                    continue
                if nums[i] == 99:
                    if nums[0] == 19690720:
                        return 100 * m + n
                    else:
                        continue

                print(i, nums[i])
                print(i + 1, nums[i + 1], nums[nums[i + 1]])
                print(i + 2, nums[i + 2], nums[nums[i + 2]])
                print(i + 3, nums[i + 3], nums[nums[i + 3]])
                print(nums)
                if nums[i] == 1:
                    nums[nums[i + 3]] = nums[nums[i + 1]] + nums[nums[i + 2]]

                else:
                    assert nums[i] == 2, f"{(i, nums[i])}"
                    nums[nums[i + 3]] = nums[nums[i + 1]] * nums[nums[i + 2]]
                # else:
                #     return nums[0] #ig?

            else:
                print("idk")


print(part2(actual_input))
