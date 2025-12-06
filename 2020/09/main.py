import numpy as np


def find_invalid(X: np.ndarray, preamble: int) -> int:
    """Function to find the invalid number"""
    # Loop over numbers after preamble
    for idx, num in enumerate(X[preamble:]):
        idx += preamble
        # Get slice of past `preamble` numbers
        X_slice = X[idx - preamble : idx]
        # Get complementary w.r.t the num
        X_comp = num - X_slice
        # Intersection gives the pair of numbers (or single)
        #  that sum up to num
        res = np.intersect1d(X_slice, X_comp)
        # If there are not at least 2 numbers, you found it!
        if res.shape[0] < 2:
            break
    return num


def find_contiguos_set(X: np.ndarray, num: int) -> int:
    """Function to find the contigous set that returns `num`
    and get the sum of its min and max"""
    # Create upper triangular matrix based on the array
    # (by repeating it across all the rows)
    Y = np.triu(
        np.array(
            [
                X,
            ]
            * X.shape[0]
        )
    )
    # Get cumsum of each rows
    Y = np.cumsum(Y, axis=1)
    # Mask the diagonal (you need at least two contiguous numbers)
    np.fill_diagonal(Y, 0)
    # Return validity mask and the corresponding row and column index(es)
    idx_row, idx_col = (Y == num).nonzero()
    # Obtain contiguous set:
    # - There is only one valid idx_row and idx_col,
    #  but numpy returns arrays. So we take the first element
    # - Add 1 to the col slice (to include the last element of the set)
    valid_slice = X[idx_row[0] : idx_col[0] + 1]
    return valid_slice.min() + valid_slice.max()


def main():
    X = np.loadtxt("2020/09/input.txt", dtype="int")
    num = find_invalid(X, preamble=25)
    print(f"Result of part 1: {num}")
    num = find_contiguos_set(X, num)
    print(f"Result of part 2: {num}")


if __name__ == "__main__":
    main()
