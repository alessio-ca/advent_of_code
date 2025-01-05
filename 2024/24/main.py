from utils import read_input_batch
import heapq
from collections import deque
import re

GatesDict = dict[str, tuple[str, set[str]]]
WiresDict = dict[str, int]
OP_DICT = {
    "OR": lambda x, y: x | y,
    "AND": lambda x, y: x & y,
    "XOR": lambda x, y: x ^ y,
}


def ordered_gates(gates: GatesDict, inputs: list[str]) -> deque[str]:
    stack = [(0, node, gates[node][1]) for node in inputs]
    queue: deque[str] = deque()
    while stack:
        i, node, node_inputs = heapq.heappop(stack)
        queue.appendleft(node)
        if any(node_in not in gates for node_in in node_inputs):
            continue
        for new_node in node_inputs:
            _, new_inputs = gates[new_node]
            heapq.heappush(stack, (i - 1, new_node, new_inputs))

    return queue


def reconstruct(wires: WiresDict) -> int:
    out_dict = sorted(
        {k: v for k, v in wires.items() if k[0] == "z"}.items(),
        key=lambda item: item[0],
    )
    return sum(
        power * value
        for power, value in zip(
            (2**i for i in range(len(wires))),
            (v for _, v in out_dict),
        )
    )


def part_1(gates: GatesDict, wires: WiresDict) -> int:
    inputs = [node for node in gates if node[0] == "z"]
    queue = ordered_gates(gates, inputs)
    while queue:
        node = queue.popleft()
        op, (in_1, in_2) = gates[node]
        wires[node] = OP_DICT[op](wires[in_1], wires[in_2])

    return reconstruct(wires)


def main(filename: str):
    wires = {
        k: int(v)
        for k, v in dict(
            line.split(": ") for line in read_input_batch(filename, line_split=False)[0]
        ).items()
    }

    gates = dict()
    for gate in read_input_batch(filename, line_split=False)[1]:
        in_1, op, in_2, out = re.findall(r"[a-zA-Z0-9]{2,3}", gate)
        gates[out] = (op, frozenset((in_1, in_2)))

    print(f"Result of part 1: {part_1(gates, wires)}")
    print(f"Result of part 2: {0}")


if __name__ == "__main__":
    main("2024/24/input.txt")
