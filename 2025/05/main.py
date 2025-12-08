from utils import read_input_batch, CoordTuple

def is_overlap(x: CoordTuple, y: CoordTuple) -> bool:
    """Check if two ranges overlap"""
    return not (x[1] < y[0] or y[1] < x[0])

def get_union(x: CoordTuple, y: CoordTuple) -> CoordTuple:
    """Get the all-inclusive union of two  ranges"""
    return (min(x[0], y[0]), max(x[1], y[1]))

def process_ranges(ranges: list[CoordTuple]) -> list[CoordTuple]:
    """Process a list of ranges to merge overlapping ones"""
    if not ranges:
        return []

    # Sort ranges by their starting point
    ranges.sort(key=lambda r: r[0])
    merged_ranges = [ranges[0]]

    for current in ranges[1:]:
        last_merged = merged_ranges[-1]
        if is_overlap(last_merged, current):
            # Merge overlapping ranges
            merged_ranges[-1] = get_union(last_merged, current)
        else:
            merged_ranges.append(current)

    return merged_ranges
    
def main(filename: str):
    raw_ranges, raw_ids = read_input_batch(filename)
    ranges: list[tuple[int,int]] =  [tuple(map(int, r.split("-"))) for r in raw_ranges]  # type: ignore
    queue = list(map(int, raw_ids))
    valid_ids = []
    assert min(queue) > 0
    for idx in queue:
        for r in ranges:
            a, b = r
            if a <= idx <= b:
                valid_ids.append(idx)
                break
    res_1 = len(valid_ids)
    print(f"Result of part 1: {res_1}")
    res_2 = 0 
    for r in process_ranges(ranges):
        res_2 += r[1] - r[0] + 1
    print(f"Result of part 2: {res_2}")

if __name__ == "__main__":
    main("2025/05/input.txt")
