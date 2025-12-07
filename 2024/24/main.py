import heapq
import re
from collections import deque
from itertools import chain

from utils import read_input_batch

GatesDict = dict[str, tuple[str, frozenset[str]]]
WiresDict = dict[str, int]
ConstructorStatus = tuple[bool, frozenset[str], str]
OP_DICT = {
    "OR": lambda x, y: x | y,
    "AND": lambda x, y: x & y,
    "XOR": lambda x, y: x ^ y,
}


def ordered_gates(gates: GatesDict, inputs: list[str]) -> deque[str]:
    # Return a deque containing the sorted gates (left to right)
    #  respecting their order
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
    # Reconstruct the value of z
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
    # Walk the queue, updating the wires dictionary
    while queue:
        node = queue.popleft()
        op, (in_1, in_2) = gates[node]
        wires[node] = OP_DICT[op](wires[in_1], wires[in_2])
    # Output the reconstructed z
    return reconstruct(wires)


def get_inputs(s: str, gates) -> list[str]:
    return sorted([gate for gate in gates if gate[0] == s])


def zero_pad(x: int) -> str:
    return str(x).zfill(2)


def swap(s: str, pair: frozenset[str]):
    in_1, in_2 = pair
    if s == in_1:
        return in_2
    elif s == in_2:
        return in_1
    else:
        return s


class AdderConstructor:
    """Construct an adder based on `gates`.
    If the construction fails, outputs the OP and INPUTS
    missing from `gates` to make the construction possible"""

    def __init__(self, gates: GatesDict):
        self.raw_gates = dict(gates)
        self.gates = {v: k for k, v in gates.items()}
        # Maps the adders's keys to the actual gates
        self.mapping: dict[str, str] = dict()
        self.max_bit = int(get_inputs("z", gates)[-1][1:]) - 1
        self.pairs: list[frozenset[str]] = []

    def map_inputs(self, inputs: frozenset[str], map_dict: dict[str, str]) -> bool:
        if all((op, inputs) in self.gates for op in map_dict):
            # Map the adder's keys to the gate
            for key, value in map_dict.items():
                self.mapping[value] = self.gates[(key, inputs)]
            return True
        else:
            return False

    def construct_start_half_adder(self):
        # The half adder has:
        #  XOR inputs --> z00
        #  AND inputs --> c00
        inputs = frozenset(("x00", "y00"))
        self.map_inputs(inputs, {"XOR": "z00", "AND": "c00"})

    def construct_full_adder(self, bit: int) -> ConstructorStatus:
        # The full adder has:
        #  XOR inputs --> a0
        #  AND inputs --> a1
        #  XOR (a0, c from previous bit) --> z
        #  AND (a0, c from previous bit) --> a2
        #  OR (a1, a2) --> c
        digit = zero_pad(bit)
        inputs = frozenset((f"x{digit}", f"y{digit}"))
        if not self.map_inputs(inputs, {"XOR": f"a0{digit}", "AND": f"a1{digit}"}):
            return False, inputs, "XOR"

        inputs = frozenset(
            (self.mapping[f"a0{digit}"], self.mapping[f"c{zero_pad(bit - 1)}"])
        )
        if not self.map_inputs(inputs, {"XOR": f"z{digit}", "AND": f"a2{digit}"}):
            return False, inputs, "XOR"

        inputs = frozenset((self.mapping[f"a1{digit}"], self.mapping[f"a2{digit}"]))
        if not self.map_inputs(inputs, {"OR": f"c{digit}"}):
            return False, inputs, "OR"

        return True, frozenset(), ""

    def construct(self) -> ConstructorStatus:
        self.construct_start_half_adder()
        for i in range(1, self.max_bit):
            out = self.construct_full_adder(i)
            # If the status is False, swap
            if not out[0]:
                _, inputs, in_op = out
                # Find the entry in self.gates that intersects the inputs and
                #  has the same
                try:
                    swap_inputs = [
                        gates
                        for (op, gates), v in self.gates.items()
                        if gates.intersection(inputs) and (op == in_op)
                    ][0]
                except IndexError:
                    raise IndexError(
                        "No swaps are possible. This system cannot represent an adder."
                    )
                pair = (swap_inputs | inputs) - (swap_inputs & inputs)
                # Reset gates
                self.raw_gates = {swap(k, pair): v for k, v in self.raw_gates.items()}
                self.gates = {v: k for k, v in self.raw_gates.items()}
                # Add pair
                self.pairs.append(pair)
                return out
        return out


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

    constructor = AdderConstructor(gates)
    status: tuple[bool, frozenset[str], str] = (False, frozenset(), "")
    # Iterate until the constructor succeeds
    while not status[0]:
        status = constructor.construct()

    print(
        f"Result of part 2: {','.join(sorted(chain.from_iterable(constructor.pairs)))}"
    )


if __name__ == "__main__":
    main("2024/24/input.txt")
