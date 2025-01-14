# https://www.codewars.com/kata/59df2f8f08c6cec835000012/train/nim
import strutils
import strformat
import std/algorithm

proc meeting*(s: string): string =
  var names: seq[tuple[first_name: string, last_name: string]] = @[]

  # Extract first and surname from given string
  for full_name in s.split(";"):
    let name_split = full_name.split(":")
    let (first_name, last_name) = (name_split[0], name_split[1])
    names &= (first_name, last_name)

  # Put all names to uppercase
  for index, name in names:
    names[index] = (name.first_name.toUpper, name.last_name.toUpper)

  # Sort names
  names.sort do(first, second: tuple[first_name: string, last_name: string]) -> int:
    result = cmp(first.last_name, second.last_name)
    if result == 0:
      result = cmp(first.first_name, second.first_name)

  # Turn seq to string again
  result = ""
  for name in names:
    result &= fmt"({name.last_name}, {name.first_name})"

if isMainModule:
  assert meeting(
    "Alexis:Wahl;John:Bell;Victoria:Schwarz;Abba:Dorny;Grace:Meta;Ann:Arno;Madison:STAN;Alex:Cornwell;Lewis:Kern;Megan:Stan;Alex:Korn"
  ) ==
    "(ARNO, ANN)(BELL, JOHN)(CORNWELL, ALEX)(DORNY, ABBA)(KERN, LEWIS)(KORN, ALEX)(META, GRACE)(SCHWARZ, VICTORIA)(STAN, MADISON)(STAN, MEGAN)(WAHL, ALEXIS)"
  assert meeting(
    "John:Gates;Michael:Wahl;Megan:Bell;Paul:Dorries;James:Dorny;Lewis:Steve;Alex:Meta;Elizabeth:Russel;Anna:Korn;Ann:Kern;Amber:Cornwell"
  ) ==
    "(BELL, MEGAN)(CORNWELL, AMBER)(DORNY, JAMES)(DORRIES, PAUL)(GATES, JOHN)(KERN, ANN)(KORN, ANNA)(META, ALEX)(RUSSEL, ELIZABETH)(STEVE, LEWIS)(WAHL, MICHAEL)"
