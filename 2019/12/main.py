from __future__ import annotations

"""
--- Day 12: The N-Body Problem ---

The space near Jupiter is not a very safe place; you need to be careful of a big
 distracting red spot, extreme radiation, and a whole lot of moons swirling around. You
  decide to start by tracking the four largest moons: Io, Europa, Ganymede, and
   Callisto.

After a brief scan, you calculate the position of each moon (your puzzle input). You
 just need to simulate their motion so you can avoid them.

Each moon has a 3-dimensional position (x, y, and z) and a 3-dimensional velocity. The
 position of each moon is given in your scan; the x, y, and z velocity of each moon
  starts at 0.

Simulate the motion of the moons in time steps. Within each time step, first update the
 velocity of every moon by applying gravity. Then, once all moons' velocities have been
  updated, update the position of every moon by applying velocity. Time progresses by
   one step once all of the positions are updated.

To apply gravity, consider every pair of moons. On each axis (x, y, and z), the
 velocity of each moon changes by exactly +1 or -1 to pull the moons together. For
  example, if Ganymede has an x position of 3, and Callisto has a x position of 5, then
   Ganymede's x velocity changes by +1 (because 5 > 3) and Callisto's x velocity
    changes by -1 (because 3 < 5). However, if the positions on a given axis are the
     same, the velocity on that axis does not change for that pair of moons.

Once all gravity has been applied, apply velocity: simply add the velocity of each moon
 to its own position. For example, if Europa has a position of x=1, y=2, z=3 and a
  velocity of x=-2, y=0,z=3, then its new position would be x=-1, y=2, z=6. This
   process does not modify the velocity of any moon.

For example, suppose your scan reveals the following positions:

<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>
Simulating the motion of these moons would produce the following:

After 0 steps:
pos=<x=-1, y=  0, z= 2>, vel=<x= 0, y= 0, z= 0>
pos=<x= 2, y=-10, z=-7>, vel=<x= 0, y= 0, z= 0>
pos=<x= 4, y= -8, z= 8>, vel=<x= 0, y= 0, z= 0>
pos=<x= 3, y=  5, z=-1>, vel=<x= 0, y= 0, z= 0>

After 1 step:
pos=<x= 2, y=-1, z= 1>, vel=<x= 3, y=-1, z=-1>
pos=<x= 3, y=-7, z=-4>, vel=<x= 1, y= 3, z= 3>
pos=<x= 1, y=-7, z= 5>, vel=<x=-3, y= 1, z=-3>
pos=<x= 2, y= 2, z= 0>, vel=<x=-1, y=-3, z= 1>

After 2 steps:
pos=<x= 5, y=-3, z=-1>, vel=<x= 3, y=-2, z=-2>
pos=<x= 1, y=-2, z= 2>, vel=<x=-2, y= 5, z= 6>
pos=<x= 1, y=-4, z=-1>, vel=<x= 0, y= 3, z=-6>
pos=<x= 1, y=-4, z= 2>, vel=<x=-1, y=-6, z= 2>

After 3 steps:
pos=<x= 5, y=-6, z=-1>, vel=<x= 0, y=-3, z= 0>
pos=<x= 0, y= 0, z= 6>, vel=<x=-1, y= 2, z= 4>
pos=<x= 2, y= 1, z=-5>, vel=<x= 1, y= 5, z=-4>
pos=<x= 1, y=-8, z= 2>, vel=<x= 0, y=-4, z= 0>

After 4 steps:
pos=<x= 2, y=-8, z= 0>, vel=<x=-3, y=-2, z= 1>
pos=<x= 2, y= 1, z= 7>, vel=<x= 2, y= 1, z= 1>
pos=<x= 2, y= 3, z=-6>, vel=<x= 0, y= 2, z=-1>
pos=<x= 2, y=-9, z= 1>, vel=<x= 1, y=-1, z=-1>

After 5 steps:
pos=<x=-1, y=-9, z= 2>, vel=<x=-3, y=-1, z= 2>
pos=<x= 4, y= 1, z= 5>, vel=<x= 2, y= 0, z=-2>
pos=<x= 2, y= 2, z=-4>, vel=<x= 0, y=-1, z= 2>
pos=<x= 3, y=-7, z=-1>, vel=<x= 1, y= 2, z=-2>

After 6 steps:
pos=<x=-1, y=-7, z= 3>, vel=<x= 0, y= 2, z= 1>
pos=<x= 3, y= 0, z= 0>, vel=<x=-1, y=-1, z=-5>
pos=<x= 3, y=-2, z= 1>, vel=<x= 1, y=-4, z= 5>
pos=<x= 3, y=-4, z=-2>, vel=<x= 0, y= 3, z=-1>

After 7 steps:
pos=<x= 2, y=-2, z= 1>, vel=<x= 3, y= 5, z=-2>
pos=<x= 1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
pos=<x= 3, y=-7, z= 5>, vel=<x= 0, y=-5, z= 4>
pos=<x= 2, y= 0, z= 0>, vel=<x=-1, y= 4, z= 2>

After 8 steps:
pos=<x= 5, y= 2, z=-2>, vel=<x= 3, y= 4, z=-3>
pos=<x= 2, y=-7, z=-5>, vel=<x= 1, y=-3, z=-1>
pos=<x= 0, y=-9, z= 6>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y= 1, z= 3>, vel=<x=-1, y= 1, z= 3>

After 9 steps:
pos=<x= 5, y= 3, z=-4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 2, y=-9, z=-3>, vel=<x= 0, y=-2, z= 2>
pos=<x= 0, y=-8, z= 4>, vel=<x= 0, y= 1, z=-2>
pos=<x= 1, y= 1, z= 5>, vel=<x= 0, y= 0, z= 2>

After 10 steps:
pos=<x= 2, y= 1, z=-3>, vel=<x=-3, y=-2, z= 1>
pos=<x= 1, y=-8, z= 0>, vel=<x=-1, y= 1, z= 3>
pos=<x= 3, y=-6, z= 1>, vel=<x= 3, y= 2, z=-3>
pos=<x= 2, y= 0, z= 4>, vel=<x= 1, y=-1, z=-1>
Then, it might help to calculate the total energy in the system. The total energy for a
 single moon is its potential energy multiplied by its kinetic energy. A moon's
  potential energy is the sum of the absolute values of its x, y, and z position
   coordinates. A moon's kinetic energy is the sum of the absolute values of its
    velocity coordinates. Below, each line shows the calculations for a moon's
     potential energy (pot), kinetic energy (kin), and total energy:

Energy after 10 steps:
pot: 2 + 1 + 3 =  6;   kin: 3 + 2 + 1 = 6;   total:  6 * 6 = 36
pot: 1 + 8 + 0 =  9;   kin: 1 + 1 + 3 = 5;   total:  9 * 5 = 45
pot: 3 + 6 + 1 = 10;   kin: 3 + 2 + 3 = 8;   total: 10 * 8 = 80
pot: 2 + 0 + 4 =  6;   kin: 1 + 1 + 1 = 3;   total:  6 * 3 = 18
Sum of total energy: 36 + 45 + 80 + 18 = 179
In the above example, adding together the total energy for all moons after 10 steps
 produces the total energy in the system, 179.

Here's a second example:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
Every ten steps of simulation for 100 steps produces:

After 0 steps:
pos=<x= -8, y=-10, z=  0>, vel=<x=  0, y=  0, z=  0>
pos=<x=  5, y=  5, z= 10>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y= -7, z=  3>, vel=<x=  0, y=  0, z=  0>
pos=<x=  9, y= -8, z= -3>, vel=<x=  0, y=  0, z=  0>

After 10 steps:
pos=<x= -9, y=-10, z=  1>, vel=<x= -2, y= -2, z= -1>
pos=<x=  4, y= 10, z=  9>, vel=<x= -3, y=  7, z= -2>
pos=<x=  8, y=-10, z= -3>, vel=<x=  5, y= -1, z= -2>
pos=<x=  5, y=-10, z=  3>, vel=<x=  0, y= -4, z=  5>

After 20 steps:
pos=<x=-10, y=  3, z= -4>, vel=<x= -5, y=  2, z=  0>
pos=<x=  5, y=-25, z=  6>, vel=<x=  1, y=  1, z= -4>
pos=<x= 13, y=  1, z=  1>, vel=<x=  5, y= -2, z=  2>
pos=<x=  0, y=  1, z=  7>, vel=<x= -1, y= -1, z=  2>

After 30 steps:
pos=<x= 15, y= -6, z= -9>, vel=<x= -5, y=  4, z=  0>
pos=<x= -4, y=-11, z=  3>, vel=<x= -3, y=-10, z=  0>
pos=<x=  0, y= -1, z= 11>, vel=<x=  7, y=  4, z=  3>
pos=<x= -3, y= -2, z=  5>, vel=<x=  1, y=  2, z= -3>

After 40 steps:
pos=<x= 14, y=-12, z= -4>, vel=<x= 11, y=  3, z=  0>
pos=<x= -1, y= 18, z=  8>, vel=<x= -5, y=  2, z=  3>
pos=<x= -5, y=-14, z=  8>, vel=<x=  1, y= -2, z=  0>
pos=<x=  0, y=-12, z= -2>, vel=<x= -7, y= -3, z= -3>

After 50 steps:
pos=<x=-23, y=  4, z=  1>, vel=<x= -7, y= -1, z=  2>
pos=<x= 20, y=-31, z= 13>, vel=<x=  5, y=  3, z=  4>
pos=<x= -4, y=  6, z=  1>, vel=<x= -1, y=  1, z= -3>
pos=<x= 15, y=  1, z= -5>, vel=<x=  3, y= -3, z= -3>

After 60 steps:
pos=<x= 36, y=-10, z=  6>, vel=<x=  5, y=  0, z=  3>
pos=<x=-18, y= 10, z=  9>, vel=<x= -3, y= -7, z=  5>
pos=<x=  8, y=-12, z= -3>, vel=<x= -2, y=  1, z= -7>
pos=<x=-18, y= -8, z= -2>, vel=<x=  0, y=  6, z= -1>

After 70 steps:
pos=<x=-33, y= -6, z=  5>, vel=<x= -5, y= -4, z=  7>
pos=<x= 13, y= -9, z=  2>, vel=<x= -2, y= 11, z=  3>
pos=<x= 11, y= -8, z=  2>, vel=<x=  8, y= -6, z= -7>
pos=<x= 17, y=  3, z=  1>, vel=<x= -1, y= -1, z= -3>

After 80 steps:
pos=<x= 30, y= -8, z=  3>, vel=<x=  3, y=  3, z=  0>
pos=<x= -2, y= -4, z=  0>, vel=<x=  4, y=-13, z=  2>
pos=<x=-18, y= -7, z= 15>, vel=<x= -8, y=  2, z= -2>
pos=<x= -2, y= -1, z= -8>, vel=<x=  1, y=  8, z=  0>

After 90 steps:
pos=<x=-25, y= -1, z=  4>, vel=<x=  1, y= -3, z=  4>
pos=<x=  2, y= -9, z=  0>, vel=<x= -3, y= 13, z= -1>
pos=<x= 32, y= -8, z= 14>, vel=<x=  5, y= -4, z=  6>
pos=<x= -1, y= -2, z= -8>, vel=<x= -3, y= -6, z= -9>

After 100 steps:
pos=<x=  8, y=-12, z= -9>, vel=<x= -7, y=  3, z=  0>
pos=<x= 13, y= 16, z= -3>, vel=<x=  3, y=-11, z= -5>
pos=<x=-29, y=-11, z= -1>, vel=<x= -3, y=  7, z=  4>
pos=<x= 16, y=-13, z= 23>, vel=<x=  7, y=  1, z=  1>

Energy after 100 steps:
pot:  8 + 12 +  9 = 29;   kin: 7 +  3 + 0 = 10;   total: 29 * 10 = 290
pot: 13 + 16 +  3 = 32;   kin: 3 + 11 + 5 = 19;   total: 32 * 19 = 608
pot: 29 + 11 +  1 = 41;   kin: 3 +  7 + 4 = 14;   total: 41 * 14 = 574
pot: 16 + 13 + 23 = 52;   kin: 7 +  1 + 1 =  9;   total: 52 *  9 = 468
Sum of total energy: 290 + 608 + 574 + 468 = 1940
What is the total energy in the system after simulating the moons given in your scan
 for 1000 steps?

--- Part Two ---

All this drifting around in space makes you wonder about the nature of the universe.
 Does history really repeat itself? You're curious whether the moons will ever return
  to a previous state.

Determine the number of steps that must occur before all of the moons' positions and
 velocities exactly match a previous point in time.

For example, the first example above takes 2772 steps before they exactly match a
 previous point in time; it eventually returns to the initial state:

After 0 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>

After 2770 steps:
pos=<x=  2, y= -1, z=  1>, vel=<x= -3, y=  2, z=  2>
pos=<x=  3, y= -7, z= -4>, vel=<x=  2, y= -5, z= -6>
pos=<x=  1, y= -7, z=  5>, vel=<x=  0, y= -3, z=  6>
pos=<x=  2, y=  2, z=  0>, vel=<x=  1, y=  6, z= -2>

After 2771 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x= -3, y=  1, z=  1>
pos=<x=  2, y=-10, z= -7>, vel=<x= -1, y= -3, z= -3>
pos=<x=  4, y= -8, z=  8>, vel=<x=  3, y= -1, z=  3>
pos=<x=  3, y=  5, z= -1>, vel=<x=  1, y=  3, z= -1>

After 2772 steps:
pos=<x= -1, y=  0, z=  2>, vel=<x=  0, y=  0, z=  0>
pos=<x=  2, y=-10, z= -7>, vel=<x=  0, y=  0, z=  0>
pos=<x=  4, y= -8, z=  8>, vel=<x=  0, y=  0, z=  0>
pos=<x=  3, y=  5, z= -1>, vel=<x=  0, y=  0, z=  0>
Of course, the universe might last for a very long time before repeating. Here's a copy
 of the second example from above:

<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
This set of initial positions takes 4686774924 steps before it repeats a previous state!
 Clearly, you might need to find a more efficient way to simulate the universe.

How many steps does it take to reach the first state that exactly matches a previous
 state?
"""
import numpy as np
from typing import List
from utils import read_input
from numba import njit
import re


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
def _perform_update(pos: np.array, vel: np.array):
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
        self.dict_states = {}
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
