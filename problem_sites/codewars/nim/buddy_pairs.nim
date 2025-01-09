# https://www.codewars.com/kata/59ccf051dcc4050f7800008f/train/nim
import std/math
import std/strutils
import strformat

proc divisors_sum(value: int): int =
  result = 0
  if value > 1:
    result += 1
  for i in 2 .. int(float(value).sqrt) + 1:
    if value mod i == 0:
      result += i
      if value div i != i:
        result += value div i

proc buddy*(start, nd: int): string =
  for i in start .. nd:
    let other = divisors_sum(i) - 1
    if other <= i:
      continue
    let other_sum = divisors_sum(other) - 1
    if other_sum == i:
      return fmt"({i} {other})"
  return "Nothing"

if isMainModule:
  assert buddy(10, 50) == "(48 75)"
  assert buddy(48, 50) == "(48 75)"
  assert buddy(1071625, 1103735) == "(1081184 1331967)"
  assert buddy(2974, 7726) == "(5775 6128)"
  assert buddy(2382, 3679) == "Nothing"
