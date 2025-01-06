class Solution:
    def bulbSwitch(self, n: int) -> int:
        if n == 0:
            return 0
        count = 0
        for i in range(1, n + 1):
            square = i**2
            if square <= n:
                count += 1
            if square > n:
                return count
        return count


if __name__ == "__main__":
    s = Solution()
    for i in range(1, 100):
        print(i, s.bulbSwitch(i))
