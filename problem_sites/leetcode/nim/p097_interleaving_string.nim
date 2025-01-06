# NOT SOLVED!
# 97
# https://leetcode.com/problems/interleaving-string/description/?envType=problem-list-v2&envId=dynamic-programming
# nim js -d:release -o:p097_pascals_triangle.js p097_pascals_triangle.nim
# nim js -d:danger -o:p097_pascals_triangle.js p097_pascals_triangle.nim
import tables

proc isInterleave(s1, s2, s3: string): bool {.exportc.} =
  var index1, index2: Positive

  # s1 = abb
  # s2 = aac
  # s3 = abaabc

when isMainModule:
  const s1_1 = "aabcc"
  const s2_1 = "dbbca"
  const s3_1 = "aadbbcbcac"
  assert true == isInterleave(s1_1, s2_1, s3_1)

#   const input2 = 1
#   const expected2: seq[seq[Positive]] = @[@[1]]
#   var calculated2 = generate(input2)
#   assert expected2 == calculated2
