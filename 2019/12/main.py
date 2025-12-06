from __future__ import annotations
import re
from typing import List

import numpy as np
from numba import njit  # type: ignore

from utils import read_input


class Moon:
    def __init__(self, x, y, z):
        self.pos = np.array([x, y, z], dtype=np.int64)
        self.vel = np.zeros(shape=self.pos.shape, dtype=np.int64)

    def update_vel(self, moon: Moon):
        # Calculate delta
        dpos = self.pos - moon.pos
        # Mask deltas of 0
        mask_zeros = dpos == 0
        # Apply condition & mask
        vel_update = np.where(dpos < 0, 1, -1)
        vel_update[mask_zeros] = 0
        # Update self and other moon's velocity
        self.vel += vel_update
        moon.vel -= vel_update

    def update_pos(self):
        self.pos += self.vel

    def kinetic_en(self):
        return np.sum(np.abs(self.vel))

    def pot_en(self):
        return np.sum(np.abs(self.pos))

    def tot_en(self):
        return self.kinetic_en() * self.pot_en()


class FullSystem:
    def __init__(self, input_list: List[List[int]]):
        self.moons = [Moon(*coords) for coords in input_list]

    def run(self, num_steps: int):
        for _ in range(num_steps):
            # Loop over the moon pairs and update velocities and pos
            for i, moon_1 in enumerate(self.moons[:-1]):
                # Update velocities
                for _, moon_2 in enumerate(self.moons[i:]):
                    moon_1.update_vel(moon_2)

                # Update pos of moon 1
                moon_1.update_pos()

            # Update pos of moon 2 (last one in the loop)
            moon_2.update_pos()

    def total_energy(self):
        return sum([moon.tot_en() for moon in self.moons])


@njit
def _perform_update(pos: np.ndarray, vel: np.ndarray):
    for i, pos1 in enumerate(pos[:-1]):
        for j, pos2 in enumerate(pos[i + 1 :]):
            delta = pos1 - pos2
            vel_update = 1 if delta < 0 else -1
            vel_update = 0 if delta == 0 else vel_update
            vel[i] += vel_update
            vel[i + 1 + j] -= vel_update

    pos += vel
    return pos, vel


class OneDimSystem:
    def __init__(self, input_list: List[int]):
        self.pos = np.array(input_list, dtype=np.int64)
        self.vel = np.zeros(shape=self.pos.shape, dtype=np.int64)
        self.dict_states: dict[tuple, int] = {}
        self.periodic = 0
        self.period = -1
        self.counter = 0
        # Record initial state
        self.record_state()

    def record_state(self):
        # Obtain state as a tuple of (pos, vel)
        state = tuple(np.concatenate([self.pos, self.vel]))
        # If state has never been seen, record it
        if state not in self.dict_states.keys():
            self.dict_states[state] = self.counter
        # Else, set the periodict state to True
        # Period is equivalent to the interval between current counter and the previous
        #  occurrence of the state
        else:
            self.periodic = 1
            self.period = self.counter - self.dict_states[state]

    def perform_update(self):
        self.pos, self.vel = _perform_update(self.pos, self.vel)

    def run(self):
        while self.periodic == 0:
            # Perform pos and vel update
            self.perform_update()
            # Update counter
            self.counter += 1
            # Record state
            self.record_state()


def main():
    input_list = read_input("2019/12/input.txt")
    # Convert into list of integers
    input_list = [list(map(int, re.findall(r"-?\d+", line))) for line in input_list]

    # For part 1, create full 3D system
    system = FullSystem(input_list)
    # Run
    system.run(1000)
    print(f"Resulf of part 1: {system.total_energy()}")

    # For part 2, create separate x, y and z arrays
    x = [row[0] for row in input_list]
    y = [row[1] for row in input_list]
    z = [row[2] for row in input_list]

    # 1D syms are enough for part 2, since the motion is decoupled between the 3
    #  dimensions (hence, periodicity can be detected by only running the sim on each
    #  axis, saving computation time)

    # Perform separate 1D syms and record the period
    period = []
    for dim in [x, y, z]:
        system = OneDimSystem(dim)
        system.run()
        period.append(system.period)

    print(f"Resulf of part 2: {np.lcm.reduce(period)}")


if __name__ == "__main__":
    main()
