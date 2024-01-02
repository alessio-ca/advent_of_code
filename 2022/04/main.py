from utils import read_input


def main(filename: str):
    X_raw = read_input(filename, line_strip=False)
    count_include = 0
    count_overlap = 0

    # Iterate over assignments
    for line in X_raw:
        inputs = []
        # Create a 2-element list containing the two pairs (also 2-element lists)
        for assignment in line.split(","):
            inputs.append([int(x) for x in assignment.split("-")])
        # Create full span of the pair, as going from max(low) to min(high)
        full_span = [max(inputs[0][0], inputs[1][0]), min(inputs[0][1], inputs[1][1])]

        # If the span is monotonic, there is overlap
        if full_span[0] <= full_span[1]:
            count_overlap += 1
            # Moreover, if the full span is one of the inputs, there is full inclusion
            if full_span in inputs:
                count_include += 1

    print(f"Result of part 1: {count_include}")
    print(f"Result of part 2: {count_overlap}")


if __name__ == "__main__":
    main("2022/04/input.txt")
