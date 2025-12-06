import numpy as np


def main():
    input_list = np.loadtxt("2019/01/input.txt", dtype=np.int64)
    print(f"Result of part 1: {np.sum(np.floor_divide(input_list, 3) - 2)}")

    overall_fuel = np.floor_divide(input_list, 3) - 2
    fuel = overall_fuel.copy()
    while np.any(fuel):
        fuel = np.floor_divide(fuel, 3) - 2
        fuel[fuel < 0] = 0
        overall_fuel = overall_fuel + fuel

    print(f"Result of part 2: {np.sum(overall_fuel)}")


if __name__ == "__main__":
    main()
