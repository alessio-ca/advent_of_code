import numpy as np
from parsimonious.grammar import Grammar, NodeVisitor  # type: ignore

from utils import read_input

# Define grammar rule for Parser
grammar = Grammar(
    r"""
    RULE = EXP (OP EXP)+
    EXP = (NUMBER / GROUP)
    GROUP = "(" RULE ")"

    NUMBER = ~r"\d+"
    OP = " " ("*" / "+") " "
"""
)


class SimpleMathVisitor(NodeVisitor):
    def visit_RULE(self, node, visited_children):
        # The first element of RULE is always a number
        # The second is a list of (OP, EXP), where OP is the math operator and EXP is
        #  everything else
        number = visited_children[0]
        for op, exp in visited_children[1]:
            # Apply math operator accordingly
            if op == "+":
                number += exp
            elif op == "*":
                number *= exp
            else:
                raise Exception(f"Operation {op} not recognized")
        return number

    def visit_EXP(self, node, visited_children):
        # EXP can be a number or an expression
        return visited_children[0]

    def visit_GROUP(self, node, visited_children):
        # GROUP's element 1 is a RULE
        return visited_children[1]

    def visit_NUMBER(self, node, visited_children):
        # Return the actual number
        return int(node.text)

    def visit_OP(self, node, visited_children):
        # Return the first element of OP (the actual operator)
        # Note that the first element itself is a list --
        #  the 0th element is the actual text
        return visited_children[1][0].text

    def generic_visit(self, node, visited_children):
        return visited_children or node


class AdvanceMathVisitor(SimpleMathVisitor):
    def visit_RULE(self, node, visited_children):
        # The first element of RULE is always a number
        # The second is a list of (OP, EXP), where OP is the math operator and EXP is
        #  everything else
        number = visited_children[0]
        grouped_calc = [number]
        for op, exp in visited_children[1]:
            # Apply math operator accordingly
            if op == "+":
                # Addition gets priority
                grouped_calc[-1] += exp
            elif op == "*":
                # Multiplication is delayed
                grouped_calc.append(exp)
            else:
                raise Exception(f"Operation {op} not recognized")
        return np.prod(grouped_calc)


def main():
    input_file = read_input("2020/18/input.txt")
    # Parse input -- basic math
    parser_basic = SimpleMathVisitor()
    parser_basic.grammar = grammar
    print(f"Result of part 1: {sum([parser_basic.parse(el) for el in input_file])}")
    # Parse input -- advanced math
    parser_advanced = AdvanceMathVisitor()
    parser_advanced.grammar = grammar
    print(f"Result of part 2: {sum([parser_advanced.parse(el) for el in input_file])}")


if __name__ == "__main__":
    main()
