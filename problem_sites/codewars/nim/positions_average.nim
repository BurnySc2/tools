# NOT SOLVED!
# https://www.codewars.com/kata/59f4a0acbee84576800000af/train/nim
import strutils
import strformat
import sequtils
import std/algorithm

import std/math
proc posAverage*(s: string): float64 =
  let s_as_seq: seq[string] = s.split(", ")
  var s_as_seq_rotated: seq[string] = s_as_seq.rotatedLeft(1)
  if s_as_seq.len == 2:
    s_as_seq_rotated = s_as_seq_rotated[0 .. s_as_seq_rotated.high - 1]

  var common: int = 0
  var total: int = s_as_seq[0].len * s_as_seq_rotated.len
  # var total: int = 0
  echo s_as_seq
  echo s_as_seq_rotated
  for index in 0 .. s_as_seq[0].high:
    for (string1, string2) in zip(s_as_seq, s_as_seq_rotated):
      # total += 1
      if string1[index] == string2[index]:
        echo fmt"{index} {string1[index]} {string2[index]}"
        common += 1

  result = 100 * common.float64 / total.float64
  echo common
  echo total
  echo result

if isMainModule:
  let max_diff = 1e-5
  # assert max_diff > abs(posAverage("4690606946, 9990494604") - 20.0)
  # assert max_diff > abs(posAverage("6900690040, 4690606946, 9990494604") - 26.666666)
  # assert max_diff >
  #   abs(
  #     posAverage(
  #       "466960, 069060, 494940, 060069, 060090, 640009, 496464, 606900, 004000, 944096"
  #     ) - 26.6666666667
  #   )
  assert max_diff >
    abs(
      posAverage(
        "444996, 699990, 666690, 096904, 600644, 640646, 606469, 409694, 666094, 606490"
      ) - 29.2592592593
    )
  assert max_diff >
    abs(
      posAverage(
        "449404, 099090, 600999, 694460, 996066, 906406, 644994, 699094, 064990, 696046"
      ) - 24.4444444444
    )
