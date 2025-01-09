# https://www.codewars.com/kata/65ba420888906c1f86e1e680
proc collinearity*(x1: int, y1: int, x2: int, y2: int): bool =
  if (x1, y1) == (0, 0) or (x2, y2) == (0, 0):
    return true
  if (x1, x2) == (0, 0) or (y1, y2) == (0, 0):
    return true

  var x_is_multiple = false
  var y_is_multiple = false
  var factor = 0

  if x1 != 0 and x2 mod x1 == 0:
    x_is_multiple = true
    factor = x2 div x1
  elif x2 != 0 and x1 mod x2 == 0:
    x_is_multiple = true
    factor = x1 div x2

  if y1 != 0 and y2 mod y1 == 0 and y2 div y1 == factor and factor != 0:
    y_is_multiple = true
  elif y2 != 0 and y1 mod y2 == 0 and y1 div y2 == factor and factor != 0:
    y_is_multiple = true

  result = x_is_multiple and y_is_multiple

when isMainModule:
  assert collinearity(1, 1, 1, 1)
  assert collinearity(1, 2, 2, 4)
  assert collinearity(1, -2, -2, 4)
  assert not collinearity(1, 1, 6, 1)
  assert collinearity(4, 0, 11, 0)
  assert not collinearity(0, 1, 6, 0)
