"""
--- Day 19: Monster Messages ---

You land in an airport surrounded by dense forest. As you walk to your high-speed train,
 the Elves at the Mythical Information Bureau contact you again. They think their
  satellite has collected an image of a sea monster! Unfortunately, the connection to
   the satellite is having problems, and many of the messages sent back from the
    satellite have been corrupted.

They sent you a list of the rules valid messages should obey and a list of received
 messages they've collected so far (your puzzle input).

The rules for valid messages (the top part of your puzzle input) are numbered and build
 upon each other. For example:

0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"
Some rules, like 3: "b", simply match a single character (in this case, b).

The remaining rules list the sub-rules that must be followed; for example, the rule 0:
 1 2 means that to match rule 0, the text being checked must match rule 1, and the text
  after the part that matched rule 1 must then match rule 2.

Some of the rules have multiple lists of sub-rules separated by a pipe (|). This means
 that at least one list of sub-rules must match. (The ones that match might be
  different each time the rule is encountered.) For example, the rule 2: 1 3 | 3 1
   means that to match rule 2, the text being checked must match rule 1 followed by
    rule 3 or it must match rule 3 followed by rule 1.

Fortunately, there are no loops in the rules, so the list of possible matches will be
 finite. Since rule 1 matches a and rule 3 matches b, rule 2 matches either ab or ba.
  Therefore, rule 0 matches aab or aba.

Here's a more interesting example:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
Here, because rule 4 matches a and rule 5 matches b, rule 2 matches two letters that
 are the same (aa or bb), and rule 3 matches two letters that are different (ab or ba).

Since rule 1 matches rules 2 and 3 once each in either order, it must match two pairs
 of letters, one pair with matching letters and one pair with different letters. This
  leaves eight possibilities: aaab, aaba, bbab, bbba, abaa, abbb, baaa, or babb.

Rule 0, therefore, matches a (rule 4), then any of the eight options from rule 1, then
 b (rule 5): aaaabb, aaabab, abbabb, abbbab, aabaab, aabbbb, abaaab, or ababbb.

The received messages (the bottom part of your puzzle input) need to be checked against
 the rules so you can determine which are valid and which are corrupted. Including the
  rules and the messages together, this might look like:

0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
Your goal is to determine the number of messages that completely match rule 0. In the
 above example, ababbb and abbbab match, but bababa, aaabbb, and aaaabbb do not,
  producing the answer 2. The whole message must match all of rule 0; there can't be
   extra unmatched characters in the message. (For example, aaaabbb might appear to
    match rule 0 above, but it has an extra unmatched b on the end.)

How many messages completely match rule 0?

--- Part Two ---

As you look over the list of messages, you realize your matching rules aren't quite
 right. To fix them, completely replace rules 8: 42 and 11: 42 31 with the following:

8: 42 | 42 8
11: 42 31 | 42 11 31
This small change has a big impact: now, the rules do contain loops, and the list of
 messages they could hypothetically match is infinite. You'll need to determine how
  these changes affect which messages are valid.

Fortunately, many of the rules are unaffected by this change; it might help to start by
 looking at which rules always match the same set of values and how those rules
  (especially rules 42 and 31) are used by the new versions of rules 8 and 11.

(Remember, you only need to handle the rules you have; building a solution that could
 handle any hypothetical combination of rules would be significantly more difficult.)

For example:

42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
Without updating rules 8 and 11, these rules only match three messages:
 bbabbbbaabaabba, ababaaaaaabaaab, and ababaaaaabbbaba.

However, after updating rules 8 and 11, a total of 12 messages match:

bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
After updating rules 8 and 11, how many messages completely match rule 0?
"""
from utils import read_input_batch
from typing import List
import re


class Rules:
    """Class for Rules entries"""

    def __init__(self, init_list: List[str], correct: bool = False):
        # Raise Exception if you don't provide a list
        if not isinstance(init_list, List):
            raise Exception(
                "Rules needs a initialization list"
                f" -- you provided a {type(init_list)}"
            )
        self.init_list = init_list
        self.parse_rules(correct)

    def parse_rules(self, correct: bool = False):
        # Pattern for rules parsing
        self.rules = {}
        for rule in self.init_list:
            idx, body = rule.split(": ")
            if '"' in body:
                # If it's a letter, take it
                body = body[1]
            else:
                body = [tuple(map(int, el.split())) for el in body.split("|")]

            self.rules[int(idx)] = body
        if correct:
            # Manually change rule 8 and 11
            self.rules[8] = [(42,), (42, 8)]
            self.rules[11] = [(42, 31), (42, 11, 31)]
        else:
            # Build a regex for rule 0 -- add anchor and end at the end
            self.the_zero_rule = "^" + self.build_rules(rule_idx=0) + "$"

    def build_rules(self, rule_idx: int):
        # Create a giga-uber-mega Regex by concatenating smaller regexes together
        #  recursively. This works if there are no recursion loops
        rule = self.rules[rule_idx]
        # Use a tracker to monitor the length of the resulting regex
        if isinstance(rule, str):
            # If this is a letter rule, just return it
            return rule

        regexes = []
        for pattern in rule:
            # For each element of rule, create a chain of regexes
            # Each pattern is piped via '|'. The expression is closed by brackets
            #  (capturing group)
            regex_group = "".join([self.build_rules(sub_idx) for sub_idx in pattern])
            regexes.append(regex_group)

        return "(" + "|".join(regexes) + ")"

    def match_rules(self, message, rule_idx: int = 0, str_index: int = 0):
        # Match rules even when recursions are possible.
        # Use an index to track where a string matches the rules.
        # Return a list of possible end indexes or an empty list if there is no match.

        # If we are past the string length, return an empty list
        if str_index >= len(message):
            return []

        rule = self.rules[rule_idx]
        if isinstance(rule, str):
            # Check if string matches the character.
            # If it does, update the indexer. Otherwise, return an empty list
            if message[str_index] == rule:
                return [str_index + 1]
            else:
                return []

        matching_str_index = []

        for pattern in rule:
            # Use the current idx to start matching
            old_matching_str_index = [str_index]
            # For each element of rule, try to match it to the possible
            #  indexers we have so far
            for sub_idx in pattern:
                new_matching_str_index = []
                for starting_idx in old_matching_str_index:
                    new_matching_str_index += self.match_rules(
                        message, sub_idx, starting_idx
                    )

                #  If it worked, keep track of the successful index(es) and continue the
                #  loop
                old_matching_str_index = new_matching_str_index

            # If the entire pattern has been matched, add it to the candidates
            matching_str_index += old_matching_str_index

        return matching_str_index


def main():
    input_file = read_input_batch("2020/19/input.txt", line_split=False)

    # Define rules
    rules = Rules(input_file[0])
    # Apply regex matching using the zero rule
    the_rule = re.compile(rules.the_zero_rule)
    print(
        "Result of part 1: "
        f"{sum(1 if the_rule.match(message) else 0 for message in input_file[1])}"
    )

    # Define rules
    rules = Rules(input_file[0], correct=True)
    # Match the rules using a custom matching that prevent recursions
    # Check that the length of the message is equal to at least one final index
    #  obtained after rule matching
    matched_rules = sum(
        [1 for message in input_file[1] if len(message) in rules.match_rules(message)]
    )
    print("Result of part 2: " f"{matched_rules}")


if __name__ == "__main__":
    main()
