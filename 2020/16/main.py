import re
from typing import List, Tuple

import numpy as np

from utils import read_input_batch


class Rules:
    """Class for Rules entries"""

    def __init__(self, init_list: List[str]):
        # Raise Exception if you don't provide a list
        if not isinstance(init_list, List):
            raise Exception(
                f"Rules needs a initialization list -- you provided a {type(init_list)}"
            )

        self.init_list = init_list
        self.parse_rules()

    def parse_rules(self):
        # Regex pattern for rules
        regex_rule = re.compile(r"^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$")
        # Define rules as a dict[str, Tuple[int,int,int,int]]
        self.rules = {}
        for rule in self.init_list:
            name, *numbers = regex_rule.match(rule).groups()
            numbers = tuple(map(int, numbers))
            self.rules[name] = numbers

    def is_ticket_valid(self, ticket: str) -> Tuple[int, list[list[int]]]:
        # Check validity of ticket entries for at least one rule
        ticket_error = 0
        checks = []
        for _, value_str in enumerate(ticket.split(",")):
            value = int(value_str)
            check = list(
                (low1 <= value <= high1) or (low2 <= value <= high2)
                for _, (low1, high1, low2, high2) in self.rules.items()
            )
            if not any(check):
                ticket_error += value

            checks.append(check)

        return ticket_error, checks


def main():
    input_file = read_input_batch("2020/16/example.txt", line_split=False)

    list_rules = input_file[0]

    my_ticket = input_file[1]
    my_ticket = my_ticket[1:]
    my_ticket = list(map(int, my_ticket[0].split(",")))

    nearby_tickets = input_file[2]
    nearby_tickets = nearby_tickets[1:]

    # Format rules
    rules = Rules(list_rules)

    # Check validity
    validity_tickets = [rules.is_ticket_valid(ticket) for ticket in nearby_tickets]

    # Return ticket error rate
    print(f"Result for part 1: {sum(error for error, _ in validity_tickets)}")

    # Retrict valid tickets and their checks
    validity_checks = [
        checks
        for error, checks in validity_tickets
        if error == 0 and all([any(check) for check in checks])
    ]
    # Convert to 3D numpy array
    # - 1st D is the ticket
    # - 2nd D is the fields in ticket
    # - 3rd D is the rule validity as they appear in rules.rules
    validity_matrix = np.array(validity_checks)

    # Compress to slices along 1D on which all fields are valid
    validity_matrix = np.all(validity_matrix, axis=0)
    # Obtain the index sorted by vailidty sum
    sorted_idx = np.argsort(validity_matrix.sum(axis=1))

    # Recursive elimination
    field_names = list(rules.rules.keys())
    field_dict = {}
    for row in range(validity_matrix.shape[0]):
        # Start from the row with the least amount of validity (1 actually)
        # Find the idx of the valid column
        idx = np.where(validity_matrix[sorted_idx][row])[0][0]
        # Assign it to the appropriate name (use the sorted index)
        field_dict[field_names[idx]] = sorted_idx[row]
        # Eliminate column
        validity_matrix[:, idx] = False

    # Obtain departure fields
    departure_fields = [name for name in field_names if "departure" in name]
    print(
        "Result for part 2: "
        f"{np.prod([my_ticket[field_dict[name]] for name in departure_fields])}"
    )


if __name__ == "__main__":
    main()
