import itertools
from collections import Counter
from typing import Dict, List, Set, Tuple

import numpy as np
from scipy.spatial.distance import cdist, pdist

from utils import read_input_batch, timefunc


def _mapping_vector_to_matrix(n: int) -> Dict[int, Tuple[int, int]]:
    """Create mapping dictionary between vector and matrix representation of
    distance pairs in a N-dimensional array"""
    dict_pairs = {}
    n_pairs = n * (n - 1) // 2
    k = 0
    j = 1
    for i in range(n_pairs):
        dict_pairs[i] = (k, j)
        j += 1
        if j == n:
            k += 1
            j = k + 1

    return dict_pairs


def _calculate_cityblock_distances(
    X: np.ndarray,
) -> Tuple[Dict[int, Set[int]], np.ndarray]:
    """Calculate all the cityblock distances between elements of a 3D array"""

    n_pairs = X.shape[1] * (X.shape[1] - 1) // 2
    # Instantiate an array that will contain all the distances per scanner
    #  in a vector representation
    dist_array = np.zeros(shape=(X.shape[0], n_pairs), dtype=int)
    # Instantiate dictionary that will contain all the unique distances per scanner
    dist_dict = {}

    # Perform calculation
    for i in range(X.shape[0]):
        dist = pdist(X[i, :, :], metric="cityblock")
        # Discard invalid elements (due to the presence of NaNs in X)
        dist_array[i, :] = np.where(dist >= 0, dist.astype(int), -1)
        # Create set of unique distances
        dist_dict[i] = set(dist_array[i, :]).difference(set([-1]))

    # Return the mapping dictionary,
    return dist_dict, dist_array


def __get_beacons(
    Y_1: np.ndarray, Y_2: np.ndarray, dict_pairs: Dict[int, Tuple[int, int]]
) -> List[int]:
    """Get the overlapping beacons between two distance arrays.
    Beacons are returned as seen by the first array"""
    # Intersect the two arrays
    intersection = np.where(np.isin(Y_1, Y_2) & (Y_1 >= 0))[0]
    # Get matrix representation
    pair_intersection: list[tuple[int, int]] = [dict_pairs[i] for i in intersection]
    # Get valid beacons
    counter = Counter([item for sublist in pair_intersection for item in sublist])
    beacons = [index for index, count in counter.items() if count >= 11]

    return beacons


def _common_beacons(
    idx_1: int,
    idx_2: int,
    dict_manh: Dict[int, Set[int]],
    dict_pairs: Dict[int, Tuple[int, int]],
    Y: np.ndarray,
) -> List:
    """Get the common beacons between two scanners"""
    # Obtain list of common cityblock distances between elements of the two scanners
    common_distances = list(dict_manh[idx_1].intersection(dict_manh[idx_2]))
    valid = []
    # For each scanner, get overlapping beacons. If there is overlap,
    #  record the valid ones
    for idx in [idx_1, idx_2]:
        beacons = __get_beacons(Y[idx, :], np.array(common_distances), dict_pairs)
        if len(beacons) < 12:
            return []
        else:
            valid.append(beacons)

    return valid


def _calculate_diff(X: np.ndarray) -> np.ndarray:
    """Compute difference in values across the dimensions"""
    diff_arr = np.zeros(shape=(X.shape[0] - 1, X.shape[1]), dtype=int)
    sorted_abs = np.argsort(X, axis=0)
    for dim in range(3):
        diff_arr[:, dim] = np.diff(X[sorted_abs[:, dim], dim])
    return diff_arr


def _align_scanners(
    X: np.ndarray, idx_1: int, idx_2: int, common_pts: List
) -> Tuple[np.ndarray, np.ndarray]:
    """Align two scanners with valid overlap"""
    # Find distances for idx_1 & idx_2
    diff_1 = _calculate_diff(X[idx_1, common_pts[0], :])
    diff_2 = _calculate_diff(X[idx_2, common_pts[1], :])

    # Align second scanner on rotation
    rotations = list(itertools.permutations(range(3)))
    for axes in rotations:
        # Find the first rotation so that all sorted differences are the same
        #  across the dimensions
        if np.all(np.sort(diff_1, axis=0) == np.sort(diff_2[:, axes], axis=0)):
            break
    X[idx_2, :, :] = X[idx_2, :, axes].T
    diff_2 = diff_2[:, axes]

    # Align second scanner on inversion by checking that the unsorted differences
    #  are the same across the dimensions
    to_flip = np.where(np.all(diff_1 == diff_2, axis=0), 1, -1)
    X[idx_2, :, :] *= to_flip

    # Find position of scanner as the difference between the min elements of the two
    #  scanners across the dimensions
    scanner_pos = X[idx_1, common_pts[0], :].min(axis=0) - X[
        idx_2, common_pts[1], :
    ].min(axis=0)

    # Align second scanner on translation
    X[idx_2, :, :] += scanner_pos
    return X, scanner_pos


@timefunc
def main():
    input_file = [
        block[1:] for block in read_input_batch("2021/19/input.txt", line_split=False)
    ]
    # Transform into 3D matrix
    input_file = [
        [list(map(int, line.split(","))) for line in block] for block in input_file
    ]
    # Fill gaps with NaNs if block have an uneven number of scanners
    max_size = max([len(block) for block in input_file])
    dim_size = len(input_file[0][0])
    X = np.empty((len(input_file), max_size, dim_size))
    X[:] = np.nan
    for i, block in enumerate(input_file):
        X[i, : len(block), :] = np.array(block)

    # Obtain mapping dictionary between vector and matrix representation
    #  of array distances
    dict_pairs = _mapping_vector_to_matrix(X.shape[1])
    # Calculate all the cityblock distances between beacons per scanner
    dict_manh, Y = _calculate_cityblock_distances(X)

    #  Align all scanners
    scanner_pos = np.zeros(shape=(X.shape[0] - 1, 3), dtype=int)
    visited = np.zeros(shape=(scanner_pos.shape[0],), dtype=int)
    roots = []
    i = 0
    # Loop until all scanners have been visited
    while not all(visited):
        # Loop over candidates
        for j in range(1, X.shape[0]):
            # Skip visited scanners
            if visited[j - 1]:
                continue
            # Obtain common beacons between root and candidate
            common_beacons = _common_beacons(i, j, dict_manh, dict_pairs, Y)
            # If there are, align scanners
            if len(common_beacons) > 0:
                X, pos = _align_scanners(X, i, j, common_beacons)
                # Add the scanner position to the array
                scanner_pos[j - 1] = pos
                # Mark candidate scanner as visited
                visited[j - 1] = 1
                # Add the root scanner to the used roots
                roots.append(i)
                # Set candidate as the new root
                i = j

                break

        # If we didn't find a match, start the sweep from the last valid root
        if len(common_beacons) == 0:
            i = roots.pop()

    # Compute the set of unique beacons
    set_beacons = set()
    for i in range(X.shape[0]):
        set_beacons.update(
            tuple(map(tuple, X[i, ~np.isnan(X[i, :, :]).any(axis=1), :].astype(int)))
        )
    print(f"Result of part 1: {len(set_beacons)}")

    # Compute the distances between the scanners
    dist = cdist(scanner_pos, scanner_pos, metric="cityblock").astype(int)
    print(f"Result of part 2: {dist.max()}")


if __name__ == "__main__":
    main()
