# https://www.codewars.com/kata/5ce399e0047a45001c853c2b/train/nim
import std/algorithm

proc partsSums*(ls: openarray[int]): seq[int] =
  result = @[0]
  var current_sum = 0
  for i in ls.reversed:
    current_sum += i
    result &= current_sum
  result.reverse

if isMainModule:
  assert partsSums(@[]) == @[0]
  assert partsSums(@[0, 1, 3, 6, 10]) == @[20, 20, 19, 16, 10, 0]
