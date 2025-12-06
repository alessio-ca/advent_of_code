import matplotlib.pyplot as plt
import networkx as nx
from parsimonious.grammar import Grammar, NodeVisitor  # type: ignore

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
    axis.set_xlim([1.1 * x for x in axis.get_xlim()])  # type: ignore
    axis.set_ylim([1.1 * y for y in axis.get_ylim()])  # type: ignore

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
