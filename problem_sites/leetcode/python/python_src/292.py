class Solution:
    cache = {i: True for i in [1, 2, 3]} | {i: False for i in [4]}

    def canWinNim(self, n: int) -> bool:
        if n in self.cache:
            return self.cache[n]
        self.cache[n] = not self.canWinNim(n - 1) or not self.canWinNim(n - 2) or not self.canWinNim(n - 3)
        return self.cache[n]


# class Solution:
#     def canWinNim(self, n: int) -> bool:
#         return n % 4 != 0

if __name__ == "__main__":
    s = Solution()

    for i in range(1, 100):
        print(i, s.canWinNim(i))
