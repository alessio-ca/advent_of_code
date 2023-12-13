from utils import read_input_batch
import re
import functools


def convert_seed_to_location(input_source, source_to_dist_maps):
    for mapping in source_to_dist_maps:
        for map_dest, map_root, map_range in mapping:
            if input_source >= map_root and input_source < map_root + map_range:
                input_source = map_dest + (input_source - map_root)
                break

    return input_source


def range_convert_source_to_dest(input_sources, mapping):
    """Create a generator over all the possible outputs for the input sources,
    given a map"""
    # Loop over individual mappings within the map
    for map_dest, map_root, map_range in mapping:
        map_end = map_root + map_range
        delta_map = map_dest - map_root
        unmapped = []
        # Loop over inputs to be mapped
        for input_root, input_end in input_sources:
            # Map can cut or "inglobate" input
            # Check if an input lower cut section
            #  (shorter than original or the original) exists
            lower_cut = (input_root, min(input_end, map_root))
            if lower_cut[1] > lower_cut[0]:
                # Lower cut is not mapped
                unmapped.append(lower_cut)

            # Check if a mapped cut exists
            middle_cut = (max(input_root, map_root), min(map_end, input_end))
            if middle_cut[1] > middle_cut[0]:
                # Map middle cut to destination for next map
                yield (middle_cut[0] + delta_map, middle_cut[1] + delta_map)

            # Check if an input higher cut section
            #  (shorter than original or original) exists
            upper_cut = (max(map_end, input_root), input_end)
            if upper_cut[1] > upper_cut[0]:
                # Upper cut is not mapped
                unmapped.append(upper_cut)
        # Update input_sources for the next map
        input_sources = unmapped
    # All the unmapped segments are propagated to the next map
    for el in unmapped:
        yield el


def main():
    mappings = read_input_batch("2023/05/input.txt", line_split=False)
    # Format mappings
    seeds = list(map(int, re.findall(r"\d+", mappings[0][0].split(": ")[1])))
    source_to_dist_maps = [
        [list(map(int, re.findall(r"\d+", mapping))) for mapping in mappings[i][1:]]
        for i in range(1, len(mappings))
    ]
    # Get locations
    locations = [convert_seed_to_location(seed, source_to_dist_maps) for seed in seeds]
    print(f"Result of part 1: {min(locations)}")

    # Apply generator to yield all possible range mappings
    total_seeds = list(
        zip(seeds[::2], (x + y for (x, y) in zip(seeds[::2], seeds[1::2])))
    )

    mapped_ranges = list(
        functools.reduce(range_convert_source_to_dest, source_to_dist_maps, total_seeds)
    )
    print(f"Result of part 2: {min(i for i,_ in mapped_ranges)}")


if __name__ == "__main__":
    main()
