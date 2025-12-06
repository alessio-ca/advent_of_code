import numpy as np

from utils import read_input


def main():
    input_num = read_input("2019/08/input.txt")
    input_num = [int(c) for c in str(input_num[0])]
    input_num = np.array(input_num)
    # Reshape into image
    width = 25
    height = 6
    layers = int(len(input_num) / (width * height))

    image = np.array(input_num).reshape(layers, height, width)
    # Get layer with fewest zero
    idx_layer = np.argmax(np.sum(image != 0, axis=(1, 2)))
    print(
        "Result of part 1: "
        f"{np.prod([(image[idx_layer] == 1).sum(), (image[idx_layer] == 2).sum()])}"
    )
    # Find layer indices of the first non-transparent element
    idx_non_2 = (image != 2).argmax(axis=0)
    # Create a 3D mask
    mask = np.zeros(shape=image.shape, dtype=np.int64)
    for (i, j), layer in np.ndenumerate(idx_non_2):
        mask[layer][i][j] = 1

    # Get final image
    image_decoded = (mask * image).sum(axis=0)
    map_to_pixel = {0: " ", 1: "#"}
    decoded = ""
    for row in image_decoded:
        decoded += "".join(map(map_to_pixel.get, row)) + "\n"

    print("Result of part 2: ")
    print("")
    print(f"{decoded}")


if __name__ == "__main__":
    main()
