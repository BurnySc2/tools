# 118
# https://leetcode.com/problems/pascals-triangle/description/?envType=problem-list-v2&envId=dynamic-programming
# nim js -d:release -o:p118_pascals_triangle.js p118_pascals_triangle.nim
# nim js -d:danger -o:p118_pascals_triangle.js p118_pascals_triangle.nim
# import tables

proc generate(numRows: int): seq[seq[Positive]] {.exportc.} =
  result = @[@[1]]
  for i in 2 .. numRows:
    var my_seq: seq[Positive] = @[1]
    var last_seq = result[^1]
    if i >= 3:
      for j in 0 .. (i - 3):
        my_seq.add(last_seq[j] + last_seq[j + 1])
    my_seq.add(1)
    result &= my_seq

# when isMainModule:
#   const input1 = 5
#   const expected1: seq[seq[Positive]] =
#     @[@[1], @[1, 1], @[1, 2, 1], @[1, 3, 3, 1], @[1, 4, 6, 4, 1]]
#   var calculated1 = generate(input1)
#   assert expected1 == calculated1

#   const input2 = 1
#   const expected2: seq[seq[Positive]] = @[@[1]]
#   var calculated2 = generate(input2)
#   assert expected2 == calculated2
