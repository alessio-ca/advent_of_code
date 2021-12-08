"""
--- Day 8: Seven Segment Search ---

You barely reach the safety of the cave when the whale smashes into the cave mouth,
 collapsing it. Sensors indicate another exit to this cave at a much greater depth, so
  you have no choice but to press on.

As your submarine slowly makes its way through the cave system, you notice that the
 four-digit seven-segment displays in your submarine are malfunctioning; they must have
  been damaged during the escape. You'll be in a lot of trouble without them, so you'd
   better figure out what's wrong.

Each digit of a seven-segment display is rendered by turning on or off any of seven
 segments named a through g:

  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
So, to render a 1, only segments c and f would be turned on; the rest would be off.
 To render a 7, only segments a, c, and f would be turned on.

The problem is that the signals which control the segments have been mixed up on each
 display. The submarine is still trying to display numbers by producing output on signal
  wires a through g, but those wires are connected to segments randomly. Worse,
   the wire/segment connections are mixed up separately for each four-digit display!
    (All of the digits within a display use the same connections, though.)

So, you might know that only signal wires b and g are turned on, but that doesn't mean
 segments b and g are turned on: the only digit that uses two segments is 1, so it must
  mean segments c and f are meant to be on. With just that information, you still can't
   tell which wire (b/g) goes to which segment (c/f). For that, you'll need to collect
    more information.

For each display, you watch the changing signals for a while, make a note of all ten
 unique signal patterns you see, and then write down a single four digit output value
  (your puzzle input). Using the signal patterns, you should be able to work out which
   pattern corresponds to which digit.

For example, here is what you might see in a single entry in your notes:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
(The entry is wrapped here to two lines so it fits; in your notes, it will all be on a
 single line.)

Each entry consists of ten unique signal patterns, a | delimiter, and finally the four
 digit output value. Within an entry, the same wire/segment connections are used (but
  you don't know what the connections actually are). The unique signal patterns
   correspond to the ten different ways the submarine tries to render a digit using the
    current wire/segment connections. Because 7 is the only digit that uses three
     segments, dab in the above example means that to render a 7, signal lines d, a, and
      b are on. Because 4 is the only digit that uses four segments, eafb means that to
       render a 4, signal lines e, a, f, and b are on.

Using this information, you should be able to work out which combination of signal wires
 corresponds to each of the ten digits. Then, you can decode the four digit output
  value. Unfortunately, in the above example, all of the digits in the output value
   (cdfeb fcadb cdfeb cdbaf) use five segments and are more difficult to deduce.

For now, focus on the easy digits. Consider this larger example:

be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb |
fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec |
fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef |
cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega |
efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga |
gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf |
gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf |
cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd |
ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg |
gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc |
fgae cfgab fg bagce
Because the digits 1, 4, 7, and 8 each use a unique number of segments, you should be
 able to tell which combinations of signals correspond to those digits. Counting only
  digits in the output values (the part after | on each line), in the above example,
   there are 26 instances of digits that use a unique number of segments (highlighted
    above).

In the output values, how many times do digits 1, 4, 7, or 8 appear?

--- Part Two ---

Through a little deduction, you should now be able to determine the remaining digits.
 Consider again the first example above:

acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab |
cdfeb fcadb cdfeb cdbaf
After some careful analysis, the mapping between signal wires and segments only make
 sense in the following configuration:

 dddd
e    a
e    a
 ffff
g    b
g    b
 cccc
So, the unique signal patterns would correspond to the following digits:

acedgfb: 8
cdfbe: 5
gcdfa: 2
fbcad: 3
dab: 7
cefabd: 9
cdfgeb: 6
eafb: 4
cagedb: 0
ab: 1
Then, the four digits of the output value can be decoded:

cdfeb: 5
fcadb: 3
cdfeb: 5
cdbaf: 3
Therefore, the output value for this entry is 5353.

Following this same process for each entry in the second, larger example above, the
 output value of each entry can be determined:

fdgacbe cefdb cefbgd gcbe: 8394
fcgedb cgb dgebacf gc: 9781
cg cg fdcagb cbg: 1197
efabcd cedba gadfec cb: 9361
gecf egdcabf bgf bfgea: 4873
gebdcfa ecba ca fadegcb: 8418
cefg dcbef fcge gbcadfe: 4548
ed bcgafe cdgba cbgef: 1625
gbdfcae bgc cg cgb: 8717
fgae cfgab fg bagce: 4315
Adding all of the output values in this larger example produces 61229.

For each entry, determine all of the wire/segment connections and decode the four-digit
 output values. What do you get if you add up all of the output values?
"""
from utils import read_input
from typing import Set, Dict, List


def _inverse_digit_mapping(
    candidate: Set[str], digits_dict: Dict[int, Set[str]]
) -> int:
    """Perform inverse mapping over a dictionary"""
    for key, value in digits_dict.items():
        if value == candidate:
            return key


def find_number(line: List[str], digit: List[str]) -> int:
    """Find the number given the signal line and digit list"""
    # Convert signal lines to sets
    line = list(map(set, line))
    # Compute the length of each signal
    length = list(map(len, line))

    digits_dict = {}
    # Assign easy digits
    digits_dict[1] = [i for (i, j) in zip(line, length) if j == 2][0]
    digits_dict[4] = [i for (i, j) in zip(line, length) if j == 4][0]
    digits_dict[7] = [i for (i, j) in zip(line, length) if j == 3][0]
    digits_dict[8] = [i for (i, j) in zip(line, length) if j == 7][0]

    # Obtain first segments definition
    #  We use the following number convention:
    #   aaaa
    #  b    c
    #  b    c
    #   dddd
    #  e    f
    #  e    f
    #   gggg
    a = digits_dict[7] - digits_dict[1]
    bd = digits_dict[4] - digits_dict[1]
    eg = digits_dict[8] - (digits_dict[4].union(digits_dict[7]))

    # Obtain 6 letters digits intersections with eight
    six_letters = set().union(
        *[digits_dict[8] - i for (i, j) in zip(line, length) if j == 6]
    )

    # Use logic to obtain all other segment definitions
    c = six_letters - (bd.union(eg))
    f = digits_dict[8] - set().union(*[a, bd, c, eg])
    e = six_letters.intersection(eg)
    d = six_letters.intersection(bd)
    b = bd - d

    # Complete the digit dictionary
    digits_dict[0] = digits_dict[8] - d
    digits_dict[2] = digits_dict[8] - b - f
    digits_dict[3] = digits_dict[8] - b - e
    digits_dict[5] = digits_dict[8] - c - e
    digits_dict[6] = digits_dict[8] - c
    digits_dict[9] = digits_dict[8] - e

    # Map digits to the digit dictionary and return the resulting number
    number_digit = int(
        "".join(
            map(
                str,
                [_inverse_digit_mapping(set(number), digits_dict) for number in digit],
            )
        )
    )
    return number_digit


def main():
    input_file = read_input("2021/08/input.txt")
    signals = []
    digits = []
    for line in input_file:
        signals.append(line.split(" | ")[0].split(" "))
        digits.append(line.split(" | ")[1].split(" "))

    # For Part 1, just find digits 2, 4, 3 or 7 long
    res_1 = sum(
        sum(len(number) in [2, 4, 3, 7] for number in entry) for entry in digits
    )
    print(f"Result of part 1: {res_1}")

    # For Part 2, we need to find the correct numbers
    total_sum = 0
    for (line, digit) in zip(signals, digits):
        # Obtain number
        num = find_number(line, digit)
        total_sum += num

    print(f"Result of part 2: {total_sum}")


if __name__ == "__main__":
    main()
