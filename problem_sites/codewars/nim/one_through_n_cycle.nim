# NOT SOLVED
# https://www.codewars.com/kata/5a057ec846d843c81a0000ad/train/nim
import std/math
import std/strutils
import std/sequtils
import strformat

proc cycle*(n: int): int =
  if gcd(n, 10) != 1:
    return -1

  var lpow = 1
  while true:
    # for i in 0..5:
    #   for j in 0..<7:
    for mpow in countdown(lpow - 1, 0, 1):
      echo fmt"{lpow} {mpow}"
      if (10 ^ lpow.uint64 - 10 ^ mpow.uint64) mod n == 0:
        return lpow - mpow
    lpow += 1
  return -1

if isMainModule:
  assert cycle(33) == 2
  assert cycle(18118) == -1
  assert cycle(69) == 22
  assert cycle(197) == 98
  assert cycle(65) == -1
