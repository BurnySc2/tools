# p3411
# https://leetcode.com/problems/maximum-subarray-with-equal-products/description/
# nim js -d:release -o:p3411.js p3411.nim
# nim js -d:danger -o:p3411.js p3411.nim
# import tables
import std/math
import std/strformat

proc maxLength(nums: seq[Natural]): Natural {.exportc.} =
  result = 1
  for lower_index, lower_value in nums:
    var
      product = lower_value
      gcd_value = lower_value
      lcm_value = lower_value
    for inner_index, next_value in nums[lower_index + 1 .. nums.high]:
      product *= next_value

      if next_value mod gcd_value != 0:
        gcd_value = gcd(gcd_value, next_value)

      if lcm_value mod next_value != 0:
        lcm_value = lcm(lcm_value, next_value)

      if product > gcd_value * lcm_value:
        break

      if product == gcd_value * lcm_value:
        let difference = inner_index + 2
        if difference > result:
          result = difference

when isMainModule:
  const input1: seq[Natural] = @[1, 2, 1, 2, 1, 1, 1]
  let result1 = maxLength(input1)
  assert result1 == 5
