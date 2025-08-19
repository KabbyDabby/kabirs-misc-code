class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:

        def get_num_subarrays(n: int):
            return n * (n + 1) // 2

        l = 0
        count = 0
        while l < len(nums):
            if nums[l] == 0:
                for i in range(1, len(nums) - l):
                    if not nums[l + i] == 0:
                        temp = i
                        break
                else:
                    temp = len(nums) - l
                print(temp)
                count += get_num_subarrays(temp)

                l += temp
            else:
                l += 1

        return count
