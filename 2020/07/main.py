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
        for child in children:
            self.graph.add_edge(parent, child[0])

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


def plot_graph(
    graph: nx.DiGraph,
    pos=None,
    node_color=None,
    with_labels=True,
    node_size=None,
    font_size=None,
    width=None,
    arrowsize=None,
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
    # List shiny_gold parent nodes
    shiny_gold_parents = list(nx.ancestors(graph, "shiny gold"))

    print(f"Result of part 1: {len(shiny_gold_parents)}")

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
