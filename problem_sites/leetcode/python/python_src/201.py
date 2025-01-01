class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        result = 0
        for bit in range(32):
            number = 2**bit
            # When a power of 2 is reached, all bits are flipped and can return 0 safely
            if left < number <= right:
                return 0

        result = 0
        for bit in range(32, -1, -1):
            number = 2**bit
            if number <= left and right < number * 2:
                left -= number
                right -= number
                result += number
        return result


if __name__ == "__main__":
    s = Solution()

    left1 = 5
    right1 = 7
    expected1 = 4
    calculated1 = s.rangeBitwiseAnd(left1, right1)
    assert expected1 == calculated1, (expected1, calculated1)

    left2 = 0
    right2 = 0
    expected2 = 0
    calculated2 = s.rangeBitwiseAnd(left2, right2)
    assert expected2 == calculated2, (expected2, calculated2)

    left3 = 1
    right3 = 2147483647
    expected3 = 0
    calculated3 = s.rangeBitwiseAnd(left3, right3)
    assert expected3 == calculated3, (expected3, calculated3)
