# p2442
# https://leetcode.com/problems/count-number-of-distinct-integers-after-reverse-operations/description/
# nim js -d:release -o:p2442.js p2442.nim
# nim js -d:danger -o:p2442.js p2442.nim
# import tables
import std/critbits
import std/unicode
import std/sequtils

proc countDistinctIntegers(nums: seq[Natural]): Natural {.exportc.} =
  var already_seen: seq[Natural] = @[]
  var tree = CritBitTree[void].default
  for i in nums:
    # Lookup if number has been seen but only if list of numbers does not exceed N
    if already_seen.len < 10:
      if already_seen.contains(i):
        continue
      else:
        already_seen.addUnique(i)

    let i_as_string: string = $i
    discard tree.containsOrIncl(i_as_string)

    # Calculate index to remove trailing zeros
    var first_non_zero = i_as_string.high
    while first_non_zero > 0:
      if i_as_string[first_non_zero] != '0':
        break
      first_non_zero -= 1

    let i_reversed = i_as_string[0 .. first_non_zero].reversed
    discard tree.containsOrIncl(i_reversed)
  result = tree.len

when isMainModule:
  const input1: seq[Natural] = @[1, 13, 10, 12, 31]
  let result1 = countDistinctIntegers(input1)
  assert result1 == 6
