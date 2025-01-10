# https://exercism.org/tracks/nim/exercises/reverse-string
proc reverse*(s: string): string =
  result = ""
  for i, _ in s:
    result &= s[s.high - i]
