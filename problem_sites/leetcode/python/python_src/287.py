from typing import List  # noqa: UP035


class Solution:
    def findDuplicate(self, nums: List[int]) -> int:  # noqa: N802, UP006
        my_list = [False for _ in nums]
        for value in nums:
            if my_list[value]:
                return value
            elif not my_list[value]:
                my_list[value] = True
        return 0
