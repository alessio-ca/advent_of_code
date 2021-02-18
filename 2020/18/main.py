"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear over
 the horizon, you are interrupted by the child sitting next to you. They're curious if
  you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you remember.

The homework (your puzzle input) consists of a series of expressions that consist of
 addition (+), multiplication (*), and parentheses ((...)). Just like normal math,
  parentheses indicate that the expression inside must be evaluated before it can be
   used by the surrounding expression. Addition still finds the sum of the numbers on
    both sides of the operator, and multiplication still finds the product.

However, the rules of operator precedence have changed. Rather than evaluating
 multiplication before addition, the operators have the same precedence, and are
  evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
      9   + 4 * 5 + 6
         13   * 5 + 6
             65   + 6
                 71
Parentheses can override this order; for example, here is what happens if parentheses
 are added to form 1 + (2 * 3) + (4 * (5 + 6)):

1 + (2 * 3) + (4 * (5 + 6))
1 +    6    + (4 * (5 + 6))
     7      + (4 * (5 + 6))
     7      + (4 *   11   )
     7      +     44
            51
Here are a few more examples:

2 * 3 + (4 * 5) becomes 26.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.
Before you can help with the homework, you need to understand it yourself. Evaluate the
 expression on each line of the homework; what is the sum of the resulting values?

--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their homework,
 but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're not the
 ones you're familiar with. Instead, addition is evaluated before multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now as
 follows:

1 + 2 * 3 + 4 * 5 + 6
  3   * 3 + 4 * 5 + 6
  3   *   7   * 5 + 6
  3   *   7   *  11
     21       *  11
         231
Here are the other examples from above:

1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
2 * 3 + (4 * 5) becomes 46.
5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.
What do you get if you add up the results of evaluating the homework problems using
 these new rules?
"""
from utils import read_input
from parsimonious.grammar import Grammar, NodeVisitor
import numpy as np

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
