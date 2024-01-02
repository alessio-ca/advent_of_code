from utils import read_input_batch


def main(filename: str):
    X_raw = read_input_batch(filename, line_split=False)
    # Convert to list of lists of integers
    X = [map(int, sublist) for sublist in X_raw]
    # Calculate the totals per elf
    X_sums = [sum(elf) for elf in X]
    print(f"Result of part 1: {max(X_sums)}")
    print(f"Result of part 2: {sum(sorted(X_sums)[-3:])}")


if __name__ == "__main__":
    main("2022/01/input.txt")
