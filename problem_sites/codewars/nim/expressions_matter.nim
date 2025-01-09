# https://www.codewars.com/kata/5ae62fcf252e66d44d00008e
import std/math

proc expressionMatter*(a, b, c: int): int =
  result = max([a + b + c, a * b * c, a + b * c, (a + b) * c, a * b + c, a * (b + c)])

if isMainModule:
  assert expressionMatter(2, 1, 2) == 6
