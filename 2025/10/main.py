from utils import read_input
import heapq
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def start_machine(machine: list[str]) -> int:
    target = [False if c=='.' else True for lights in machine[0] for c in list(lights)][1:-1]
    buttons = [tuple(map(int, line[1:-1].split(','))) for line in machine[1:-1]]

    heap = [(0, [0]*len(target))]
    visited = set()
    while heap:
        steps, lights = heapq.heappop(heap)
        if tuple(lights) in visited:
            continue
        visited.add(tuple(lights))
        if lights == target:
            return steps
        
        for button in buttons:
            new_lights = lights[:]
            for b in button:
                new_lights[b] = not new_lights[b]
            heapq.heappush(heap, (steps+1, new_lights))
    return -1

def jolt_machine(machine: list[str]) -> int:
    """Match target joltages using integer linear programming."""
    target = list(map(int, machine[-1][1:-1].split(',')))
    buttons = [tuple(map(int, line[1:-1].split(','))) for line in machine[1:-1]]
    
    # Create constraint matrix A where A[i,j] = 1 if button j affects target i
    A = np.zeros((len(target), len(buttons)), dtype=np.int64)
    for button_idx, button in enumerate(buttons):
        for jolter_idx in button:
            A[jolter_idx, button_idx] = 1
    
    # Objective: minimize sum of button presses (each button has cost 1)
    c = np.ones(len(buttons))
    # Constraints: A @ x == target
    constraints = LinearConstraint(A, lb=target, ub=target)
    # Bounds: x >= 0 (non-negative button presses)
    bounds = Bounds(lb=0., ub=np.inf)
    # Solve 
    result = milp(c=c, constraints=constraints, bounds=bounds, integrality=np.ones(len(buttons), dtype=int))
    if not result.success:
        return -1
    else:
        return int(np.round(result.x).sum())

def main(filename: str):
    data = [line.split() for line in read_input(filename)]
    start_steps = [start_machine(machine) for machine in data]
    print(f"Result of part 1: {sum(start_steps)}")
    jolt_steps = [jolt_machine(machine) for machine in data]
    print(f"Result of part 2: {sum(jolt_steps)}")

 
if __name__ == "__main__":
    main("2025/10/input.txt")
