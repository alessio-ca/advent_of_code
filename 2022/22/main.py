from utils import read_input
import math
import re
import itertools

DIR_MAP = {"right": 0, "down": 1, "left": 2, "up": 3}


def find_match(c, line):
    try:
        return line.index(c)
    except ValueError:
        return math.inf


class Node:
    def __init__(self, c, v, id):
        self.x, self.y = c
        self.v = v
        self.id = id

        # Initialise neighs
        self.up = None
        self.up_flip = None
        self.down = None
        self.down_flip = None
        self.right = None
        self.right_flip = None
        self.left = None
        self.left_flip = None


class LinkedNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None

    def insert_after(self, ref_node, new_node):
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_at_end(self, new_node):
        if self.head is None:
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.head.prev, new_node)


def create_node_system(input_file, size):
    dict_nodes = {}
    idx = -1
    counter = 0
    for i, line in enumerate(input_file[:-2]):
        offset = min(find_match(".", line), find_match("#", line))
        line = line.strip()

        chunks = [line[x : x + size] for x in range(0, len(line), size)]
        for block, chunk in enumerate(chunks):
            for j, c in enumerate(chunk):
                coords = (block * size + j + offset, i)
                dict_nodes[coords] = Node(coords, c, idx + 1 + block)

        counter += 1
        if (counter % size) == 0:
            counter = 0
            idx += 1 * (len(line) // size)
    # Populate directions
    for idx in [0, 1]:
        gen = [coord[idx] for coord in dict_nodes.keys()]
        min_c, max_c = min(gen), max(gen)
        for i in range(min_c, max_c + 1):
            array = [key for key in dict_nodes.keys() if key[idx] == i]
            array.sort(key=lambda x: x[0])
            for low, high in zip(array, array[1:] + array[:1]):
                if idx == 0:
                    setattr(dict_nodes[low], "down", high)
                    setattr(dict_nodes[high], "up", low)
                else:
                    setattr(dict_nodes[low], "right", high)
                    setattr(dict_nodes[high], "left", low)
    return dict_nodes


def walk_maze(dict_nodes, instructions, dirlist):
    pos = (min(x for x, y in dict_nodes.keys() if y == 0), 0)
    for move in instructions:
        if isinstance(move, int):
            # Attempt move
            for _ in range(move):
                new_pos = getattr(dict_nodes[pos], dirlist.head.value)
                if dict_nodes[new_pos].v == ".":
                    pos = new_pos
                else:
                    break

        else:
            # Rotate
            if move == "R":
                dirlist.head = dirlist.head.next
            else:
                dirlist.head = dirlist.head.prev
    return pos


def main():
    input_file = read_input("2022/22/input.txt", line_strip=False)
    dict_nodes = create_node_system(input_file, 4)

    llist = CircularDoublyLinkedList()
    for val in DIR_MAP.keys():
        llist.insert_at_end(LinkedNode(val))

    steps = list(map(int, re.findall(r"\d+", input_file[-1].strip())))
    rot = re.findall(r"[A-Z]", input_file[-1].strip())

    instructions = [
        x for x in itertools.chain(*itertools.zip_longest(steps, rot)) if x is not None
    ]

    pos = walk_maze(dict_nodes, instructions, llist)
    res = 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + DIR_MAP[llist.head.value]
    print(f"Result of part 1: {res}")


if __name__ == "__main__":
    main()
