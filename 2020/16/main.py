"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the legs of
 your re-routed trip coming up is on a high-speed train. However, the train ticket you
  were given is in a language you don't understand. You should probably figure out what
   it says before you get to the train station after the next flight.

Unfortunately, you can't actually read the words on the ticket. You can, however, read
 the numbers, and so you figure out the fields these tickets must have and the valid
  ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the numbers on
 other nearby tickets for the same train service (via the airport security cameras)
  together into a single document you can reference (your puzzle input).

The rules for ticket fields specify a list of fields that exist somewhere on the ticket
 and the valid ranges of values for each field. For example, a rule like class: 1-3 or
  5-7 means that one of the fields in every ticket is named class and can be any value
   in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are both valid in this field,
    but 4 is not).

Each ticket is represented by a single line of comma-separated values. The values are
 the numbers on the ticket in the order they appear; every ticket has the same format.
  For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'
Here, ? represents text in a language you don't understand. This ticket might be
 represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual train
  tickets you're looking at are much more complicated. In any case, you've extracted
   just the numbers in such a way that the first number is always the same specific
    field, the second number is always a different specific field, and so on - you just
     don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets that
 contain values which aren't valid for any field. Ignore your ticket for now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
It doesn't matter which position corresponds to which field; you can identify invalid
 nearby tickets by considering only whether tickets contain values that are not valid
  for any field. In this example, the values on the first nearby ticket are all valid
   for at least one field. This is not true of the other three nearby tickets: the
    values 4, 55, and 12 are are not valid for any field. Adding together all of the
     invalid values produces your ticket scanning error rate: 4 + 55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket scanning
 error rate?

--- Part Two ---

Now that you've identified which tickets contain invalid values, discard those tickets
 entirely. Use the remaining valid tickets to determine which field is which.

Using the valid ranges for each field, determine what order the fields appear on the
 tickets. The order is consistent between all tickets: if seat is the third field, it
  is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
Based on the nearby tickets in the above example, the first position must be row, the
 second position must be class, and the third position must be seat; you can conclude
  that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket that
 start with the word departure. What do you get if you multiply those six values
  together?
"""
from utils import read_input_batch
from typing import List, Tuple
import re
import numpy as np


class Rules:
    """Class for Rules entries"""

    def __init__(self, init_list: List[str]):
        # Raise Exception if you don't provide a list
        if not isinstance(init_list, List):
            raise Exception(
                "Rules needs a initialization list"
                f" -- you provided a {type(init_list)}"
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

    def is_ticket_valid(self, ticket: str) -> Tuple[int, List[Tuple[int]]]:
        # Check validity of ticket entries for at least one rule
        ticket_error = 0
        checks = []
        for i, value in enumerate(ticket.split(",")):
            value = int(value)
            check = list(
                (low1 <= value <= high1) or (low2 <= value <= high2)
                for _, (low1, high1, low2, high2) in self.rules.items()
            )
            if not any(check):
                ticket_error += value

            checks.append(check)

        return ticket_error, checks


def main():
    input_file = read_input_batch("2020/16/input.txt", line_split=False)

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
    print("Result for part 1: " f"{sum(error for error,_ in validity_tickets)}")

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
