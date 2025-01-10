# TODO: Could not submit solution, exit code 1 for some reason, maybe fixed later
# https://www.codewars.com/kata/55a29405bc7d2efaff00007c
proc going*(n: int): float64 =
  #  1! + 2! + 3!   3!   2!   1!
  # ------------- = -- + -- + --
  #       3!        3!   3!   3!
  var fact_sum = 1.float64
  var factor = n
  const limit = 1e-7
  for i in countdown(n - 1, 1, 1):
    let term: float64 = 1 / factor.float64
    factor *= i
    fact_sum += term
    if term < limit:
      break
  fact_sum

if isMainModule:
  let limit = 1e-6
  assert going(5) == 1.275
  assert abs(going(30) - 1.034525) < limit
