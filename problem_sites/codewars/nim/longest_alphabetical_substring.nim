# https://www.codewars.com/kata/5a7f58c00025e917f30000f1/train/nim
proc longest*(str: string): string =
  var longest_string = ""
  var current_string = ""

  var last_char = ' '
  for char in str:
    if last_char == ' ' or last_char.ord <= char.ord:
      current_string &= char
    else:
      if longest_string.len < current_string.len:
        longest_string = current_string
      current_string = "" & char
    last_char = char

  if longest_string.len < current_string.len:
    longest_string = current_string

  result = longest_string

if isMainModule:
  assert longest("nab") == "ab"
  assert longest("abcdeapbcdef") == "abcde"
  assert longest("asdfaaaabbbbcttavvfffffdf") == "aaaabbbbctt"
