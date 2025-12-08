from utils import read_input

def find_invalid_ids(repeat_n: int, ranges: list[tuple[str, str]]) -> list[int]:
    invalid_ids: list[int] = []
    for start, end in ranges:
        if len(end) % repeat_n == 0:
            unit = end[:(len(end) // repeat_n)] 
        else:
            unit = '9' * (len(end) // repeat_n)

        if len(unit) == 0:
            continue
        if int(unit * repeat_n) > int(end):
            unit = str(int(unit) - 1)
        while (idx:=int(unit * repeat_n)) >= int(start):
            invalid_ids.append(idx)
            unit = str(int(unit) - 1)
    return invalid_ids       

def main(filename: str):
    raw_ranges: list[tuple[str, str]] = [tuple(line.split('-')) for line in read_input(filename)[0].split(',')]  # type: ignore[misc]
    invalid_ids_1 = find_invalid_ids(2, raw_ranges)
    print(f"Result of part 1: {sum(invalid_ids_1)}")
    max_size = max(len(end) for _, end in raw_ranges)
    invalid_ids_2 = set([x  for repeat_n in range(2, max_size + 1) for x in find_invalid_ids(repeat_n, raw_ranges)])
    print(f"Result of part 2: {sum(invalid_ids_2)}")

if __name__ == "__main__":
    main("2025/02/input.txt")
