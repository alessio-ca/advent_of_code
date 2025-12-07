import numpy as np

from utils import read_input


def minimize_fuel(X: np.ndarray, constant_rate: bool) -> float:
    """Simple function to optimize fuel consumption"""
    # Define initial guess for min_fuel (overestimate)
    min_fuel = X.sum() if constant_rate else int((X * (X + 1) * 0.5).sum())

    # Define limits for the line search
    # One can demonstrate that the optimal fuel value is bounded by the mean of X via:
    # X_mean - 0.5 <= i <= X_mean + 0.5
    X_mean = X.mean()
    min_pos, max_pos = int(np.floor(X_mean - 0.5)), int(np.ceil(X_mean + 0.5))

    # Perform line search
    for i in range(min_pos, max_pos):
        # Define the absolute step number between candidate position and any crab
        X_temp = np.abs(X - i)
        # Optimize min_fuel. For the constant_rate case, use the simple sum. For the non
        #  constant_rate case, use the Gaussian sum.
        min_fuel = (
            min(min_fuel, X_temp.sum())
            if constant_rate
            else min(min_fuel, int((X_temp * (X_temp + 1) * 0.5).sum()))
        )

    return min_fuel


def main():
    input_file = list(map(int, read_input("2021/07/input.txt")[0].split(",")))
    X = np.array(input_file, dtype=int)

    print(f"Result of part 1: {minimize_fuel(X, constant_rate=True)}")
    print(f"Result of part 2: {minimize_fuel(X, constant_rate=False)}")


if __name__ == "__main__":
    main()
