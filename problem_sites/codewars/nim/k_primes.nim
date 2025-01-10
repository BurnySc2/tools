# TODO Solution times out!
# Timed OutExit Code: 1

# https://www.codewars.com/kata/5726f813c8dcebf5ed000a6b/train/nim
import std/tables
import std/sequtils
import std/algorithm
import std/math

# Cache for k
var cache: Table[int, seq[int]] = initTable[int, seq[int]]()

proc sieve(n: int) =
  # Early return if cached list is already larger than n
  if 1 in cache:
    let current_k1 = cache[1]
    if current_k1.len > 0:
      let last_value = current_k1[^1]
      if last_value >= n:
        return

  var my_array: seq[bool] = newSeqWith(n + 1, true)
  my_array[0] = false
  my_array[1] = false
  # +1 at the loop max?
  for index in 2 .. n.float.sqrt.int:
    if my_array[index] == true:
      for index2 in countup(index * 2, my_array.high, index):
        my_array[index2] = false

  var primes_k_eq_1: seq[int] = @[]
  for index, is_prime in my_array:
    if is_prime == true:
      primes_k_eq_1 &= index
  cache[1] = primes_k_eq_1

proc calc_cache_for_k(k, nd: int) =
  sieve(nd)
  for i in 2 .. k:
    # Continue if seq for 'k=i' already in cache, skip calculation
    if i in cache:
      let my_cache = cache[i]
      if my_cache.len > 0:
        let last_value = my_cache[^1]
        if last_value >= nd:
          continue

    var cache_for_k: seq[int] = @[]
    for prime1 in cache[i - 1]:
      if nd < prime1:
        break
      for prime2 in cache[1]:
        let value = prime1 * prime2
        if nd < value:
          break
        cache_for_k &= value
    cache_for_k.sort
    cache_for_k = cache_for_k.deduplicate(isSorted = true)
    cache[i] = cache_for_k

proc countKprimes*(k, start, nd: int): seq[int] =
  calc_cache_for_k(k, nd)
  result = @[]
  for i in cache[k]:
    if nd < i:
      break
    if start <= i:
      result &= i

proc puzzle*(s: int): int =
  result = 0
  if s < 2 + 8 + 128:
    return 0
  calc_cache_for_k(7, s)
  for c in cache[7]:
    if s < c:
      continue
    for b in cache[3]:
      let b_c = b + c
      if s < b_c:
        continue
      for a in cache[1]:
        let a_b_c = a + b_c
        if s < a_b_c:
          continue
        if s == a_b_c:
          result += 1

if isMainModule:
  assert countKprimes(5, 1000, 1100) ==
    @[1020, 1026, 1032, 1044, 1050, 1053, 1064, 1072, 1092, 1100]
  assert countKprimes(5, 500, 600) == @[500, 520, 552, 567, 588, 592, 594]
  assert countKprimes(7, 1000, 1500) ==
    @[1008, 1056, 1080, 1088, 1120, 1200, 1216, 1248, 1458, 1472]

  assert puzzle(100) == 0
  assert puzzle(151) == 3
