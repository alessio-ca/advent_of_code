import numpy as np

from utils import read_input


def main():
    input_file = read_input("2020/13/input.txt")

    timestamp = int(input_file[0])
    #  Mark invalid buses with 0
    array_buses = np.array(
        [int(bus) if bus != "x" else 0 for bus in input_file[1].split(",")]
    )
    # For part 1:
    buses = array_buses[array_buses > 0]
    buses_state = buses - timestamp % buses
    print(f"Result of part 1: {buses_state.min() * buses[np.argmin(buses_state)]}")

    # For part 2:
    # Create 2D array with:
    # - Bus array
    # - Position array
    bus_matrix = np.stack([array_buses, np.arange(array_buses.shape[0])], axis=1)

    #  Sort descending -- highest bus number first
    sorted_idx = np.argsort(-bus_matrix[:, 0])
    bus_matrix = bus_matrix[sorted_idx]
    # Remove the invalid buses (they are marked with 0)
    bus_matrix = bus_matrix[bus_matrix[:, 0] > 0]

    # Initialize search of the timestamp
    #  Start from 0 and a 1-shift
    timestamp = 0
    shift = 1
    for bus, offset in bus_matrix:
        # Find first time that satisfies condition
        while (timestamp + offset) % bus:
            # Until condition is not set, keep shifting the timestamp
            timestamp += shift
        # Update shift to be
        #  the least-common-multiple between previous shift and bus
        shift = np.lcm(shift, bus)
    print(f"Result of part 2: {timestamp}")


if __name__ == "__main__":
    main()
