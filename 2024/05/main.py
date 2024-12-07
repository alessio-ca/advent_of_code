from utils import read_input_batch
from collections import defaultdict


def rule_enforcer(
    rules_dict: dict[int, set[int]], updates: list[int]
) -> tuple[int, int]:

    sum_correct = 0
    sum_incorrect = 0

    for update in updates:
        i = 0
        is_correct = True
        # Scroll through the update
        while i < len(update):
            # Check if intersection between future pages and set of rules
            #  for current page is empty
            if set(update[i:]).intersection(rules_dict[update[i]]):
                # If not, flag & push the current index to end of update
                is_correct = False
                update = update[:i] + update[i + 1 :] + [update[i]]
            else:
                i += 1

        if is_correct:
            sum_correct += update[len(update) // 2]
        else:
            sum_incorrect += update[len(update) // 2]

    return sum_correct, sum_incorrect


def main(filename: str):
    rules, updates = read_input_batch(filename)
    rules = list(map(lambda x: list(map(int, x.split("|"))), rules))
    updates = list(map(lambda x: list(map(int, x.split(","))), updates))
    # Create a dictionary of rules: each page maps to the set of
    # "future" pages according to the rules (right --> left)
    rules_dict = defaultdict(set)
    for i, j in rules:
        rules_dict[j].add(i)

    sum_correct, sum_incorrect = rule_enforcer(rules_dict, updates)

    print(f"Result of part 1: {sum_correct}")
    print(f"Result of part 2: {sum_incorrect}")


if __name__ == "__main__":
    main("2024/05/input.txt")
