# https://www.codewars.com/kata/5a5f9f80f5dc3f942b002309/train/nim
type Omnibool = object

proc `==`*[T](o: Omnibool, b: T): bool =
  result = true

const omnibool*: Omnibool = Omnibool()
