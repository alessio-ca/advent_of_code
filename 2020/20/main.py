"""
--- Day 20: Jurassic Jigsaw ---

The high-speed train leaves the forest and quickly carries you south. You can even see
 a desert in the distance! Since you have some spare time, you might as well see if
  there was anything interesting in the image the Mythical Information Bureau satellite
   captured.

After decoding the satellite messages, you discover that the data actually contains
 many small images created by the satellite's camera array. The camera array consists
  of many cameras; rather than produce a single square image, they produce many smaller
   square image tiles that need to be reassembled back into a single image.

Each camera in the camera array returns a single monochrome image tile with a random
 unique ID number. The tiles (your puzzle input) arrived in a random order.

Worse yet, the camera array appears to be malfunctioning: each image tile has been
 rotated and flipped to a random orientation. Your first task is to reassemble the
  original image by orienting the tiles so they fit together.

To show how the tiles should be reassembled, each tile's image data includes a border
 that should line up exactly with its adjacent tiles. All tiles have this border, and
  the border lines up exactly when the tiles are both oriented correctly. Tiles at the
   edge of the image also have this border, but the outermost edges won't line up with
    any other tiles.

For example, suppose you have the following nine tiles:

Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
By rotating, flipping, and rearranging them, you can find a square arrangement that
 causes all adjacent borders to line up:

#...##.#.. ..###..### #.#.#####.
..#.#..#.# ###...#.#. .#..######
.###....#. ..#....#.. ..#.......
###.##.##. .#.#.#..## ######....
.###.##### ##...#.### ####.#..#.
.##.#....# ##.##.###. .#...#.##.
#...###### ####.#...# #.#####.##
.....#..## #...##..#. ..#.###...
#.####...# ##..#..... ..#.......
#.##...##. ..##.#..#. ..#.###...

#.##...##. ..##.#..#. ..#.###...
##..#.##.. ..#..###.# ##.##....#
##.####... .#.####.#. ..#.###..#
####.#.#.. ...#.##### ###.#..###
.#.####... ...##..##. .######.##
.##..##.#. ....#...## #.#.#.#...
....#..#.# #.#.#.##.# #.###.###.
..#.#..... .#.##.#..# #.###.##..
####.#.... .#..#.##.. .######...
...#.#.#.# ###.##.#.. .##...####

...#.#.#.# ###.##.#.. .##...####
..#.#.###. ..##.##.## #..#.##..#
..####.### ##.#...##. .#.#..#.##
#..#.#..#. ...#.#.#.. .####.###.
.#..####.# #..#.#.#.# ####.###..
.#####..## #####...#. .##....##.
##.##..#.. ..#...#... .####...#.
#.#.###... .##..##... .####.##.#
#...###... ..##...#.. ...#..####
..#.#....# ##.#.#.... ...##.....
For reference, the IDs of the above tiles are:

1951    2311    3079
2729    1427    2473
2971    1489    1171
To check that you've assembled the image correctly, multiply the IDs of the four corner
 tiles together. If you do this with the assembled tiles from the example above, you
  get 1951 * 3079 * 2971 * 1171 = 20899048083289.

Assemble the tiles into an image. What do you get if you multiply together the IDs of
 the four corner tiles?
"""
from utils import read_input_batch
import numpy as np

TILE_CHAR = "#"
ZERO_CHAR = "."


def find_neighbors(X_ids, X):
    # For each tile, create a dictionary of the possible edge candidates
    # Need tuple conversion since arrays and lists are not hashable
    dict_edges = {
        k: set.union(
            *[
                {tuple(edge), tuple(np.flip(edge))}
                for edge in [tile[0, :], tile[-1, :], tile[:, 0], tile[:, -1]]
            ]
        )
        for k, tile in zip(X_ids, X)
    }
    dict_neighbours = {
        k: (
            {
                k_neigh
                for k_neigh, edges_neigh in dict_edges.items()
                if edge & edges_neigh
            }
            - {k}
        )
        for k, edge in dict_edges.items()
    }
    return dict_neighbours


def find_corners(dict_neighbours):
    # Corners have only 2 neighbors
    return [
        idx
        for idx, edge_neighbours in dict_neighbours.items()
        if len(edge_neighbours) == 2
    ]


def main():
    input_file = read_input_batch("2020/20/example.txt")
    #  Preprocess inputs
    id_list = [int(tile[1][:-1]) for tile in input_file]
    tile_list = [tile[2:] for tile in input_file]

    # Convert characters to 1 and 0, and to array
    X_ids = np.array(id_list, dtype=int)
    X = np.array(
        [
            [[1 if char == TILE_CHAR else 0 for char in line] for line in tile]
            for tile in tile_list
        ],
        dtype=int,
    )

    # Find neighbours for each edge
    dict_neighbours = find_neighbors(X_ids, X)
    # Find the corner edges
    corner_edges = find_corners(dict_neighbours)
    # Return result
    print(f"Result of part 1: {np.prod(corner_edges)}")


if __name__ == "__main__":
    main()
