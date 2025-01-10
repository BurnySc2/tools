# https://www.codewars.com/kata/5541f58a944b85ce6d00006a/train/nim
# import std/tables
# import std/sequtils

# [0, 1, 1, 2, 3, 5, 8, ...]
var fib_numbers_cache: seq[uint64] = @[0'u64, 1'u64]

proc productFib*(prod: uint64): seq[uint64] =
  result = @[]
  if prod == 0:
    return @[0'u64, 1'u64, 1'u64]
  var
    index = 1
    small_fib = 0'u64
    large_fib = 1'u64

  while true:
    index += 1
    if fib_numbers_cache.len == index:
      fib_numbers_cache &= small_fib + large_fib

    small_fib = large_fib
    large_fib = fib_numbers_cache[index]
    let fib_product: uint64 = small_fib * large_fib

    if prod <= fib_product:
      result = @[small_fib, large_fib, uint64(prod == fib_product)]
      break

if isMainModule:
  assert productFib(4895'u64) == @[55'u64, 89'u64, 1]
  assert productFib(5895'u64) == @[89'u64, 144'u64, 0]
  assert productFib(74049690'u64) == @[6765'u64, 10946'u64, 1]
