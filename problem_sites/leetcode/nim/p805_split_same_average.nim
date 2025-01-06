# NOT SOLVED!
# 805
# https://leetcode.com/problems/split-array-with-same-average/description/?envType=problem-list-v2&envId=dynamic-programming
# nim js -d:release -o:p805_split_same_average.js p805_split_same_average.nim
# nim js -d:danger -o:p805_split_same_average.js p805_split_same_average.nim
# import tables
import math
# import std/strformat

proc can_be_split(
    nums: seq[Natural],
    current_numbers: seq[Natural],
    current_index: Natural,
    target_average: float32,
): bool =
  if nums.len == current_numbers.len:
    return false
  if current_numbers.len > 0 and
      current_numbers.sum.toFloat / current_numbers.len.toFloat == target_average:
    return true
  for i in current_index .. nums.high:
    let r = can_be_split(nums, current_numbers & nums[i], i + 1, target_average)
    if r == true:
      return true
  return false

proc splitArraySameAverage(nums: seq[Natural]): bool {.exportc.} =
  if nums.len <= 1:
    return false
  let average = nums.sum.toFloat / nums.len.toFloat
  return can_be_split(nums, @[], 0, average)

# when isMainModule:
#   const input1: seq[Natural] = @[1, 2, 3, 4, 5, 6, 7, 8]
#   assert true == splitArraySameAverage(input1)

#   const input2: seq[Natural] = @[3, 1]
#   assert false == splitArraySameAverage(input2)
