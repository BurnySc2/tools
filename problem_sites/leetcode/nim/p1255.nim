# NOT SOLVED, problem with javascript: key cant be string with CountTable or Table?
# CritBitTree also having issues when creating a copy, deepcopy not available when converting to js

# p1255
# https://leetcode.com/problems/maximum-score-words-formed-by-letters/description/
# nim js -d:release -o:p1255.js p1255.nim
# nim js -d:danger -o:p1255.js p1255.nim
# import std/math
import std/strformat
# import std/tables
# import std/algorithm
import std/sequtils
import std/strutils
import std/critbits

proc `<=`(t1: CritBitTree[int], t2: CritBitTree[int]): bool =
  result = true
  for string1, count1 in t1:
    if string1 notin t2 or t2[string1] < count1:
      return false

proc copy(t: CritBitTree[int]): CritBitTree[int] =
  result = CritBitTree[int].default
  for key, value in t:
    result[key] = value

proc `-`(t: CritBitTree[int], w: string): CritBitTree[int] =
  # Implementation for removing a word from CountTable and returning a copy
  # TODO Write a copy function
  result = t.copy
  for char in w:
    assert result[$char] > 0
    if result[$char] == 1:
      result.excl($char)
      continue
    result[$char] = result[$char] - 1

proc inc(t: var CritBitTree[int], w: string) =
  for letter in w:
    if t.containsOrIncl($letter, 1):
      t[$letter] = t[$letter] + 1

proc can_use_word(letter_count_table: CritBitTree[int], word: string): bool =
  var current_word_count_table = CritBitTree[int].default
  current_word_count_table.inc(word)
  # echo fmt"Comparing: {current_word_count_table} <= {letter_count_table}"
  result = current_word_count_table <= letter_count_table

proc help(
    result_list: seq[tuple[score: int, list_of_words: seq[string]]],
    available_words: seq[string],
    letter_count_table: CritBitTree[int],
    words_to_score_table: CritBitTree[int],
): seq[tuple[score: int, list_of_words: seq[string]]] =
  discard
    """
    loop over each available word (from words to score table)
      check if we have all available letters to insert the word
        add word to each list of combinations and update score

        then call this function again with
        - word table but this word is removed (only useable once!)
        - letters table subtracted (minus currently used word)
  """
  result = @[]
  for index, word in available_words:
    if letter_count_table.can_use_word(word):
      # Add word with score to result list
      let word_score = words_to_score_table[word]
      var new_result_list: seq[tuple[score: int, list_of_words: seq[string]]] =
        @[(word_score, @[word])]
      for entry in result_list:
        new_result_list &= (entry.score + word_score, entry.list_of_words & word)
      result &= new_result_list

      let reduced_letter_count_table = letter_count_table - word
      var reduced_available_words: seq[string] =
        available_words[index + 1 .. available_words.high]
      echo fmt"Available words to use: {reduced_available_words}"
      echo fmt"Current word list: {result}"
      echo fmt"Current letter list: {reduced_letter_count_table}"
      echo ""
      result &=
        help(
          new_result_list, reduced_available_words, reduced_letter_count_table,
          words_to_score_table,
        )

proc maxScoreWords(
    words: seq[string], letters: seq[string], score: seq[int]
): int {.exportc.} =
  # # Convert letters to CountTable
  # # https://nim-lang.org/docs/tables.html#basic-usage-counttable
  var letter_count_table: CritBitTree[int] = CritBitTree[int].default
  for letter in letters:
    letter_count_table.inc(letter)
  # echo fmt"Initial letter count table: {letter_count_table}"

  # # Assign score for each word
  var letter_score_table: CritBitTree[int] = CritBitTree[int].default
  # echo LowercaseLetters.toSeq
  for index, letter in LowercaseLetters.toSeq:
    letter_score_table[$letter] = score[index]

  var word_score_table: CritBitTree[int] = CritBitTree[int].default
  for word in words:
    var value = 0
    for character in word:
      # echo $character
      if $character in letter_score_table:
        value += letter_score_table[$character]
    word_score_table[word] = value
  echo fmt"Word score table: {word_score_table}"
  echo fmt"Words order: {words}"

  # Sort words by score value (descending)
  # words.sort do(word1, word2: string) -> int:
  #   let
  #     word1_score = word_score_table[word1]
  #     word2_score = word_score_table[word2]
  #   cmp(word2_score, word1_score)

  let result_list = help(@[], words, letter_count_table, word_score_table)

  # Return best result
  result = 0
  for entry in result_list:
    echo fmt"Final entry: {entry}"
    if result < entry.score:
      result = entry.score
  return result

when isMainModule:
  let words = @["dog", "cat", "dad", "good"]
  let letters = @["a", "a", "c", "d", "d", "d", "g", "o", "o"]
  let score =
    @[1, 0, 9, 5, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  let result1 = maxScoreWords(words, letters, score)
  assert result1 == 23
