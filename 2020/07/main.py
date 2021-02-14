"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact,
 it looks like you'll even have time to grab some food: all flights are
  currently delayed due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being
 enforced about bags and their contents; bags must be color-coded and must
  contain specific quantities of other color-coded bags. Apparently, nobody
   responsible for these regulations considered how long they would take to
    enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
These rules specify the required contents for 9 bag types. In this example,
 every faded blue bag is empty, every vibrant plum bag contains 11 bags (5
  faded blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag,
 how many different bag colors would be valid for the outermost bag? (In other
  words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

A bright white bag, which can hold your shiny gold bag directly.
A muted yellow bag, which can hold your shiny gold bag directly, plus some
 other bags.
A dark orange bag, which can hold bright white and muted yellow bags, either
 of which could then hold your shiny gold bag.
A light red bag, which can hold bright white and muted yellow bags, either of
 which could then hold your shiny gold bag.
So, in this example, the number of bag colors that can eventually contain at
 least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag?
 (The list of rules is quite long; make sure you get all of it.)

--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices,
 but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

faded blue bags contain 0 other bags.
dotted black bags contain 0 other bags.
vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black
 bags.
dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black
 bags.
So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags
 within it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1
  + 1*7 + 2 + 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper
 than this example; be sure to count all of the bags, even if the nesting
  becomes topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.
In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""

from parsimonious.grammar import Grammar, NodeVisitor
import networkx as nx
import matplotlib.pyplot as plt

# Define grammar rule for Parser
grammar = Grammar(
    r"""
    TEXT = RULE+
    RULE = (ENTRY / EMPTY)

    EMPTY = PARENT "no other bags." "\n"?
    ENTRY = PARENT CHILDREN "." "\n"?

    PARENT = COLOR " bags contain "
    CHILDREN = CHILD+
    CHILD = NUMBER " " COLOR " " BAG SEP

    NUMBER = ~r"\d+"
    COLOR = ~r"\w+ \w+"
    BAG = (~r"\b(bag)\b" / ~r"\b(bags)\b")
    SEP = ~r"(, |(?=\.))"

"""
)


# Parser Class
class MyVisitor(NodeVisitor):
    # Create a Networkx graph
    def create_graph(self, *args, **kwargs):
        self.graph = nx.DiGraph()
        super().parse(*args, **kwargs)
        return self.graph

    def visit_ENTRY(self, node, visited_children):
        parent, children, *_ = visited_children
        # Add a graph edge between parent and children
        for color, number in children:
            self.graph.add_edge(parent, color, count=number)

    def visit_PARENT(self, node, visited_children):
        # This returns the 0-th element of PARENT, COLOR
        return visited_children[0]

    def visit_CHILD(self, node, visited_children):
        # This returns a tuple of (COLOR, NUMBER)
        return visited_children[2], visited_children[0]

    def visit_NUMBER(self, node, visited_children):
        return int(node.text)

    def visit_COLOR(self, node, visited_children):
        color = node.text
        # Add a graph node being the color
        self.graph.add_node(color)
        return color

    def generic_visit(self, node, visited_children):
        return visited_children or node


def count_bags(graph: nx.DiGraph, bag: str):
    """Count the number of bags contained in a particular bag
    Considers the children of this bag as well!
    """
    # The bag itself counts as 1
    count = 1
    for child in graph.neighbors(bag):
        count += count_bags(graph, child) * graph.edges[bag, child]["count"]

    return count


def plot_graph(
    graph: nx.DiGraph,
    pos=None,
    node_color="#1f78b4",
    with_labels=True,
    edge_labels=None,
    node_size=300,
    font_size=12,
    width=1,
    arrowsize=10,
    alpha=None,
    out_file="graph.png",
):
    nx.draw_networkx(
        graph,
        pos=pos,
        node_color=node_color,
        with_labels=with_labels,
        node_size=node_size,
        font_size=font_size,
        width=width,
        arrowsize=arrowsize,
        alpha=alpha,
    )

    plt.axis("off")
    axis = plt.gca()
    axis.set_xlim([1.1 * x for x in axis.get_xlim()])
    axis.set_ylim([1.1 * y for y in axis.get_ylim()])

    plt.savefig(out_file, bbox_inches="tight", dpi=1200)


def main():
    # Open raw file
    input_raw = open("2020/07/input.txt", "r")

    # Create graph by parsing input
    parser = MyVisitor()
    parser.grammar = grammar
    graph = parser.create_graph(input_raw.read())

    # List of shiny_gold parent nodes
    shiny_gold_parents = list(nx.ancestors(graph, "shiny gold"))
    print(f"Result of part 1: {len(shiny_gold_parents)}")

    # Count bags contained in a shiny_gold bag
    # The -1 is to remove itself from the count
    bags_in_shiny_gold = count_bags(graph, "shiny gold") - 1
    print(f"Result of part 2: {bags_in_shiny_gold}")

    # Optional: plot the graph!
    colors = []
    for item in graph.nodes.keys():
        if item == "shiny gold":
            colors.append("gold")
        elif item in shiny_gold_parents:
            colors.append("red")
        else:
            colors.append("blue")

    plot_graph(
        graph,
        pos=nx.spring_layout(graph, k=0.5),
        node_color=colors,
        with_labels=True,
        alpha=0.5,
        node_size=1,
        font_size=0.1,
        width=0.01,
        arrowsize=2,
        out_file="2020/07/graph_input.png",
    )


if __name__ == "__main__":
    main()
