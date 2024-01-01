from utils import read_input
from utils import timefunc
from collections import defaultdict, deque


class Record:
    def __init__(self, record, groups) -> None:
        self.record = record
        self.groups = tuple(map(int, groups.split(",")))

    def count_configs(self):
        # Initialize count dict
        init = (0, 0)
        cache_dict = defaultdict(int)
        cache_dict[init] = 1
        for c in self.record:
            # For each new letter, keep queue of:
            # - group_id (group of #)
            # - group size (how many #)
            # - group count (how many permutations have reached this group)
            queue = deque([])
            # Iterate over cache_dict
            for (group_id, group_size), group_count in cache_dict.items():
                if c in "?.":
                    # If c is (possibly) '.',
                    #  test if group is empty or group is correct
                    if group_size == 0:
                        queue.append((group_id, group_size, group_count))
                    elif group_size == self.groups[group_id]:
                        queue.append((group_id + 1, 0, group_count))
                if c in "?#":
                    # If c is (possibly) '#',
                    #  test if group can keep growing
                    if (
                        group_id < len(self.groups)
                        and group_size < self.groups[group_id]
                    ):
                        queue.append((group_id, group_size + 1, group_count))

            # Clear the dictionary to remove invalid paths
            cache_dict.clear()
            for group_id, group_size, group_count in queue:
                cache_dict[(group_id, group_size)] += group_count

        return sum(
            count
            for (gid, size), count in cache_dict.items()
            if gid == len(self.groups)
            or (gid == len(self.groups) - 1 and size == self.groups[gid])
        )


@timefunc
def main(filename: str):
    records = [Record(*line.split()) for line in read_input(filename)]
    total_n = 0
    for record in records:
        total_n += record.count_configs()
    print(f"Result of part 1: {total_n}")

    for record in records:
        record.record = "?".join([record.record for _ in range(5)])
        record.groups *= 5
    total_n = 0
    for record in records:
        total_n += record.count_configs()
    print(f"Result of part 2: {total_n}")


if __name__ == "__main__":
    main("2023/12/input.txt")
