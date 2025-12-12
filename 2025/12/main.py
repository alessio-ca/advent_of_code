from utils import read_input_batch
import numpy as np

def main(filename: str):
    data = read_input_batch(filename, line_split=False)
    shape_sizes = np.array([[1 if c == '#' else 0 for line in shape[1:] for c in list(line)] for shape in data[:-1]]).sum(axis=1)
    grid_sizes = np.array([list(map(int, line[0].split('x'))) for line in  [tree.split(': ') for tree in data[-1]]])
    present_sets = np.array([list(map(int, line[1].split())) for line in  [tree.split(': ') for tree in data[-1]]])
    grid_area = (grid_sizes).prod(axis=1)
    required_area = (present_sets*shape_sizes[np.newaxis, :]).sum(axis=1)
    ratio = np.where(present_sets.sum(axis=1) > 2, required_area / grid_area <= 0.8, required_area / grid_area <= 0.9)
    print(f"Result of part 1: {ratio.sum()}")


if __name__ == "__main__":
    main("2025/12/input.txt")
