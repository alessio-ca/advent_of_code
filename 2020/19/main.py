import re
from typing import List

from utils import read_input_batch


class Rules:
    """Class for Rules entries"""

    def __init__(self, init_list: List[str], correct: bool = False):
        # Raise Exception if you don't provide a list
        if not isinstance(init_list, List):
            raise Exception(
                f"Rules needs a initialization list -- you provided a {type(init_list)}"
            )
        self.init_list = init_list
        self.parse_rules(correct)

    def parse_rules(self, correct: bool = False):
        # Pattern for rules parsing
        self.rules = {}
        for rule in self.init_list:
            body: str | list[tuple[int, ...]]
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
    print(f"Result of part 2: {matched_rules}")


if __name__ == "__main__":
    main()
