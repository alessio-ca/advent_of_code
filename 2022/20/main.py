from utils import read_input, timefunc
from collections import deque


def mix_match(dict_input, n_mix):
    mix_X = deque((k, v) for k, v in dict_input.items())
    for _ in range(n_mix):
        for k, v in dict_input.items():
            # Rotate list left by the amount corresponding to
            #  the index of the (k,v) tuple
            mix_X.rotate(-mix_X.index((k, v)))
            # Pop the (k,v) element and rotate left by v
            mix_X.rotate(-mix_X.popleft()[1])
            # Insert the (k,v) element at the left end
            mix_X.appendleft((k, v))

    # Obtain the index of the target element (0)
    target_idx = [v for _, v in mix_X].index(0)
    # Return
    return sum(mix_X[(target_idx + k) % len(mix_X)][1] for k in [1000, 2000, 3000])


@timefunc
def main(filename: str):
    X = list(map(int, read_input(filename, line_strip=True)))
    Y = list(range(len(X)))

    dict_input = {k: v for k, v in zip(Y, X)}
    print(f"Result of part 1: {mix_match(dict_input, 1)}")

    dec_key = 811589153
    dict_input = {k: v * dec_key for k, v in zip(Y, X)}
    print(f"Result of part 2: {mix_match(dict_input, 10)}")


if __name__ == "__main__":
    main("2022/20/input.txt")
