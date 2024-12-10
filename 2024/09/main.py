from utils import read_single_line, timefunc
from collections import deque, defaultdict
import heapq


def compactify(diskmap: list[int]) -> int:
    assert len(diskmap) % 2 != 0
    gaps = deque(
        (i + 1) % 2 == 0 for i, size in enumerate(diskmap[1:]) for _ in range(size)
    )
    digits = deque((i + 1) for i, size in enumerate(diskmap[2::2]) for _ in range(size))

    disksum = 0
    # Start from end of 0 block
    i = diskmap[0]

    while digits:
        gap = gaps.popleft()
        # If gap is True, it's a number
        if gap:
            disksum += i * digits.popleft()
        # Otherwise, it's a blank
        else:
            disksum += i * digits.pop()

        i += 1
    return disksum


def compactify_v2(diskmap: list[int]) -> int:
    assert len(diskmap) % 2 != 0
    digits: deque[tuple[int, int, int]] = deque(
        []
    )  # queue of idx, block_size and digit_id
    gaps: defaultdict[int, list[int]] = defaultdict(list)  # dict of gap_size -> indexes
    # Start from end of 0 block
    k = diskmap[0]
    # Populate digits queue and gaps dictionary
    for i, (gap, digit) in enumerate(zip(diskmap[1::2], diskmap[2::2])):
        if gap > 0:
            gaps[gap].append(k)
        digits.append((k + gap, digit, i + 1))
        k += gap + digit

    disksum = 0

    while digits:
        # Extract digit
        d_i, d_size, d = digits.pop()
        # Find candidate gaps
        candidates: list[tuple[int, int]] = []
        heapq.heapify(candidates)
        for g_size, g_idxs in gaps.items():
            # Gap needs to be larger than digit
            if g_size >= d_size:
                g_i = heapq.heappop(g_idxs)
                # Gap needs to be prior to digit
                if g_i > d_i:
                    heapq.heappush(g_idxs, g_i)
                    continue
                else:
                    heapq.heappush(candidates, (g_i, g_size))

        # Extract gap index and size
        if candidates:
            idx, size = heapq.heappop(candidates)
            # Add new gap to left if needed
            if (residual := size - d_size) > 0:
                heapq.heappush(gaps[residual], idx + d_size)
            # Exhaust the other candidates
            while candidates:
                g_i, g_size = heapq.heappop(candidates)
                heapq.heappush(gaps[g_size], g_i)

        # Return the digit index otherwise
        else:
            idx = d_i

        # Update disksum
        disksum += sum(d * i for i in range(idx, idx + d_size))

    return disksum


@timefunc
def main(filename: str):
    diskmap = list(map(int, read_single_line(filename)))
    print(f"Result of part 1: {compactify(diskmap)}")
    print(f"Result of part 2: {compactify_v2(diskmap)}")


if __name__ == "__main__":
    main("2024/09/input.txt")
