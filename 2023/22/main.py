from __future__ import annotations
from utils import read_input
from typing import Tuple, List, Set
from collections import defaultdict
import heapq
from typing import TypeVar

T = TypeVar("T", bound=int)
Coord = Tuple[T, T, T]
Cube = Tuple[Coord, Coord]


class BrickSystem:
    def __init__(self, bricks: List[Cube]) -> None:
        self.og_bricks = sorted(bricks, key=lambda v: v[0][2])
        self.settled = defaultdict(int)
        # Parents need to remain a complete set
        self.parents = {i: set() for i in range(len(bricks))}
        self.children = defaultdict(set)
        self.free_pieces = set()

    def create_cubes(self) -> List[Set[Coord]]:
        return [
            {
                (x, y, z)
                for x in range(x1, x2 + 1)
                for y in range(y1, y2 + 1)
                for z in range(z1, z2 + 1)
            }
            for (x1, y1, z1), (x2, y2, z2) in self.og_bricks
        ]

    def intersect_after_move(self, move_down) -> bool:
        """Check intersection after a move down"""
        return any(cube in self.settled for cube in move_down)

    def free_fall(self):
        bricks = self.create_cubes()
        for i, brick in enumerate(bricks):
            # Attempt a move
            move_down = {(x, y, z - 1) for x, y, z in brick}

            # Check if move intersects the system
            while not self.intersect_after_move(move_down) and not any(
                pos[-1] == 0 for pos in move_down
            ):
                # Continue to move down
                brick = move_down
                move_down = {(x, y, z - 1) for x, y, z in brick}

            # Intersection cubes correspond to the brick's parents
            intersected = {
                self.settled[cube] for cube in move_down if cube in self.settled
            }

            self.settled |= {pos: i for pos in brick}
            for parent in intersected:
                self.parents[parent].add(i)
                self.children[i].add(parent)

    def disintegrate(self) -> int:
        """Check how many pieces don't have children,
        or their children have more than one parent"""
        for parent, children in self.parents.items():
            if not children or all(len(self.children[child]) > 1 for child in children):
                self.free_pieces.add(parent)

        return len(self.free_pieces)

    def single_reaction(self, seed: int) -> int:
        """Starting from seed, do a disintegration reaction"""
        seeds = [seed]
        heapq.heapify(seeds)
        disintegrated = set()
        chain_reaction = 0
        while seeds:
            seed = heapq.heappop(seeds)
            disintegrated.add(seed)
            for child in self.parents[seed]:
                # Check if all parents are gone
                if not (self.children[child] - disintegrated):
                    heapq.heappush(seeds, child)
                    chain_reaction += 1
        return chain_reaction

    def chain_reaction(self):
        return sum(
            [
                self.single_reaction(key)
                for key in self.parents
                if key not in self.free_pieces
            ]
        )


def main(filename: str):
    brick_system = BrickSystem(
        [
            [list(map(int, seq.split(","))) for seq in line.split("~")]
            for line in read_input(filename)
        ]
    )
    brick_system.free_fall()
    print(f"Result of part 1: {brick_system.disintegrate()}")
    print(f"Result of part 2: {brick_system.chain_reaction()}")


if __name__ == "__main__":
    main("2023/22/input.txt")
