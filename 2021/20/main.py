import numpy as np
from scipy.ndimage import convolve

from utils import read_input_batch

MAP_DICT = {".": 0, "#": 1}
INVERSE_MAP_DICT = {0: ".", 1: "#"}


def _image_enhance(
    image: np.ndarray, filter: np.ndarray, algorithm: np.ndarray, rounds: int
) -> np.ndarray:
    k = 0
    for _ in range(rounds):
        # Pad the input image with constant value k
        temp_image = np.pad(image, (1, 1), "constant", constant_values=k)
        # Convolve with constant value k
        temp_conv = convolve(temp_image, filter, mode="constant", cval=k)
        # Apply algo to the image
        image = algorithm[temp_conv]
        # Calculate new constant by taking the convolution of the previous constant
        new_k = convolve(
            k * np.ones((1, 1), dtype=int), filter, mode="constant", cval=k
        )[0, 0]
        # Set constant to the algorithm of the new constant
        k = algorithm[new_k]

    return image


def main():
    input_file = read_input_batch("2021/20/input.txt")
    algorithm, image = (
        [*map(MAP_DICT.get, "".join([el for el in input_file[0]]))],
        [[*map(MAP_DICT.get, line)] for line in input_file[1]],
    )
    # Convert to Numpy arrays
    algorithm = np.array(algorithm, dtype=int)
    image = np.array(image, dtype=int)
    filter = 2 ** np.arange(9).reshape(3, 3)
    Y = image.copy()
    print(f"Result of part 1: {_image_enhance(Y, filter, algorithm, 2).sum()}")
    print(f"Result of part 2: {_image_enhance(Y, filter, algorithm, 50).sum()}")


if __name__ == "__main__":
    main()
