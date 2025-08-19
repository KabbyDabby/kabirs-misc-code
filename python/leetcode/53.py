from math import inf


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        curr = 0
        ret = -inf

        for num in nums:
            curr = max(num, curr + num)

            ret = max(ret, curr)

        return ret
