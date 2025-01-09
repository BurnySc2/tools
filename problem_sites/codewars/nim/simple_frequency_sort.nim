# https://www.codewars.com/kata/5a8d2bf60025e9163c0000bc
import std/tables
import std/algorithm

proc solve*(arr: openArray[int]): seq[int] =
  var counter = initTable[int, Natural]()
  for i in arr:
    counter[i] = counter.getOrDefault(i, 0) + 1

  result = @arr
  result.sort do(x, y: int) -> int:
    if counter[x] == counter[y]:
      return cmp(y, x)
    cmp(counter[x], counter[y])
  result.reverse

if isMainModule:
  assert solve([2, 3, 5, 3, 7, 9, 5, 3, 7]) == [3, 3, 3, 5, 5, 7, 7, 2, 9]
  assert solve([1, 2, 3, 0, 5, 0, 1, 6, 8, 8, 6, 9, 1]) ==
    [1, 1, 1, 0, 0, 6, 6, 8, 8, 2, 3, 5, 9]
