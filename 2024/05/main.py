from collections import defaultdict, deque

from utils import read_input_batch


def rule_enforcer(
    rules_dict: dict[int, set[int]], updates: list[list[int]]
) -> tuple[int, int]:
    sum_correct = 0
    sum_incorrect = 0
    for update in updates:
        queue = deque(update)
        ordered: deque[int] = deque()
        # Scroll through the queue
        while queue:
            # Pop a page & check if intersection of queue with rules is empty
            page = queue.pop()
            if set(queue).intersection(rules_dict[page]):
                # If not, flag & push the current page to end of queue
                queue.appendleft(page)
            else:
                # Append page to ordered
                ordered.append(page)

        value = list(ordered)[len(update) // 2]
        if list(ordered) == update:
            sum_correct += value
        else:
            sum_incorrect += value

    return sum_correct, sum_incorrect


def main(filename: str):
    rules_raw, updates_raw = read_input_batch(filename)
    rules = list(map(lambda x: list(map(int, x.split("|"))), rules_raw))
    updates = list(map(lambda x: list(map(int, x.split(","))), updates_raw))
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
