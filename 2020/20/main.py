from __future__ import annotations

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

--- Part Two ---

Now, you're ready to check the image for sea monsters.

The borders of each tile are not part of the actual image; start by removing them.

In the example above, the tiles become:

.#.#..#. ##...#.# #..#####
###....# .#....#. .#......
##.##.## #.#.#..# #####...
###.#### #...#.## ###.#..#
##.#.... #.##.### #...#.##
...##### ###.#... .#####.#
....#..# ...##..# .#.###..
.####... #..#.... .#......

#..#.##. .#..###. #.##....
#.####.. #.####.# .#.###..
###.#.#. ..#.#### ##.#..##
#.####.. ..##..## ######.#
##..##.# ...#...# .#.#.#..
...#..#. .#.#.##. .###.###
.#.#.... #.##.#.. .###.##.
###.#... #..#.##. ######..

.#.#.### .##.##.# ..#.##..
.####.## #.#...## #.#..#.#
..#.#..# ..#.#.#. ####.###
#..####. ..#.#.#. ###.###.
#####..# ####...# ##....##
#.##..#. .#...#.. ####...#
.#.###.. ##..##.. ####.##.
...###.. .##...#. ..#..###
Remove the gaps to form the actual image:

.#.#..#.##...#.##..#####
###....#.#....#..#......
##.##.###.#.#..######...
###.#####...#.#####.#..#
##.#....#.##.####...#.##
...########.#....#####.#
....#..#...##..#.#.###..
.####...#..#.....#......
#..#.##..#..###.#.##....
#.####..#.####.#.#.###..
###.#.#...#.######.#..##
#.####....##..########.#
##..##.#...#...#.#.#.#..
...#..#..#.#.##..###.###
.#.#....#.##.#...###.##.
###.#...#..#.##.######..
.#.#.###.##.##.#..#.##..
.####.###.#...###.#..#.#
..#.#..#..#.#.#.####.###
#..####...#.#.#.###.###.
#####..#####...###....##
#.##..#..#...#..####...#
.#.###..##..##..####.##.
...###...##...#...#..###
Now, you're ready to search for sea monsters! Because your image is monochrome, a sea
 monster will look like this:

                  #
#    ##    ##    ###
 #  #  #  #  #  #
When looking for this pattern in the image, the spaces can be anything; only the # need
 to match. Also, you might need to rotate or flip your image before it's oriented
  correctly to find sea monsters. In the above image, after flipping and rotating it to
   the appropriate orientation, there are two sea monsters (marked with O):

.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#
Determine how rough the waters are in the sea monsters' habitat by counting the number
 of # that are not part of a sea monster. In the above example, the habitat's water
  roughness is 273.

How many # are not part of a sea monster?


"""
from utils import read_input_batch, read_input
import numpy as np
from typing import Set
import itertools
from scipy.signal import correlate2d

TILE_CHAR = "#"
ZERO_CHAR = "."


def rotate_and_flip(X: np.array):
    """Convenience function to rotate and flip an array"""
    list_rot_and_flip = []
    X_temp = X.copy()
    for _ in range(2):
        for _ in range(4):
            X_temp = np.rot90(X_temp)
            list_rot_and_flip.append(X_temp)
        X_temp = np.flip(X_temp, axis=1)
    return list_rot_and_flip


class Tile:
    """Class for tiles"""

    def __init__(self, idx: int, X: np.array):
        self.id = idx
        self.X = X

    def is_above(self, tile: Tile):
        return np.array_equal(self.X[-1, :], tile.X[0, :])

    def is_left(self, tile: Tile):
        return np.array_equal(self.X[:, -1], tile.X[:, 0])


class Map:
    """Class for Map instance"""

    def __init__(self, X_ids: np.array, X_tiles: np.array):
        self.grid_size = int(np.sqrt(len(X_tiles)))
        # Create dictionary of tiles (complete with rotation and flipping
        # Each ID is associated to the eight possible tiles after flipping and rotation
        self.tiles = {
            idx: [Tile(idx, trans_tile) for trans_tile in rotate_and_flip(tile)]
            for idx, tile in zip(X_ids, X_tiles)
        }
        # Obtain dictionary of neighbours
        self.neighbours = self.find_neighbors()
        # Find corners
        self.corners = self.find_corners()
        # Find edges
        self.edges = self.find_edges()
        # Initialize map
        self.grid_map = [
            [None for i in range(self.grid_size)] for i in range(self.grid_size)
        ]
        # Obtain dictionary of valid tiles for map
        self.candidate_tiles = self.valid_tiles()
        # Reconstruct map
        self.search_position(0, 0, set())
        self.map = np.concatenate(
            [
                np.concatenate(
                    [tile.X[1:-1, 1:-1] for tile in self.grid_map[i][:]], axis=1
                )
                for i in range(self.grid_size)
            ],
            axis=0,
        )

    def find_neighbors(self):
        # For each tile, create a dictionary of the edge candidates.
        # Loop through the 8 rotated-flipped versions of a tile and select the top edge
        # Need tuple conversion since arrays and lists are not hashable
        dict_edges = {
            k: {tuple(tile.X[0, :]) for tile in tiles}
            for k, tiles in self.tiles.items()
        }
        # For each tile, get the set of tiles that are possible neighbours
        # For two tiles to be neighbors, their sets of edges must intersect
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

    def find_corners(self):
        # Corners have only 2 neighbors
        return [
            idx
            for idx, edge_neighbours in self.neighbours.items()
            if len(edge_neighbours) == 2
        ]

    def find_edges(self):
        # Edges have only 2 or 3 neighbors
        return [
            idx
            for idx, edge_neighbours in self.neighbours.items()
            if len(edge_neighbours) == 3
        ]

    def is_corner(self, row_id: int, col_id: int):
        return (row_id in [0, self.grid_size - 1]) & (col_id in [0, self.grid_size - 1])

    def not_corner(self, row_id: int, col_id: int, idx: int):
        return (
            (row_id in [0, self.grid_size - 1])
            & (col_id in [0, self.grid_size - 1])
            & (idx not in self.corners)
        )

    def is_edge(self, row_id: int, col_id: int):
        return (row_id in [0, self.grid_size - 1]) | (col_id in [0, self.grid_size - 1])

    def valid_tiles(self):
        # Create dictionary of valid tiles per grid position
        candidate_tiles = {}
        for (row_id, col_id) in itertools.product(range(self.grid_size), repeat=2):
            if self.is_corner(row_id, col_id):
                candidate_tiles[(row_id, col_id)] = set(self.corners)
            elif self.is_edge(row_id, col_id):
                candidate_tiles[(row_id, col_id)] = set(self.edges)
            else:
                candidate_tiles[(row_id, col_id)] = (
                    set(self.tiles.keys()) - set(self.edges) - set(self.corners)
                )
        return candidate_tiles

    def search_position(self, row_id: int, col_id: int, visited_tiles: Set(int)):
        # If you are at the edge, return
        if row_id == self.grid_size:
            return

        # Obtain valid tiles
        valid_tiles = self.candidate_tiles[(row_id, col_id)] - visited_tiles
        # Scan all tiles
        for idx, tiles in self.tiles.items():
            #  If not valid, continue
            if idx not in valid_tiles:
                continue
            # If valid position, check that tile is valid neighbor to the above and
            #  left tiles in grid map
            if row_id > 0:
                above_tile = self.grid_map[row_id - 1][col_id].id
                if idx not in self.neighbours[above_tile]:
                    continue

            if col_id > 0:
                left_tile = self.grid_map[row_id][col_id - 1].id
                if idx not in self.neighbours[left_tile]:
                    continue

            # If valid candidate, find right orientation
            for tile in tiles:
                if row_id > 0:
                    if not self.grid_map[row_id - 1][col_id].is_above(tile):
                        continue
                if col_id > 0:
                    if not self.grid_map[row_id][col_id - 1].is_left(tile):
                        continue

                # Assign position and add ID to visited_tiles
                self.grid_map[row_id][col_id] = tile
                visited_tiles.add(tile.id)

                # Recursive search
                if col_id == self.grid_size - 1:
                    self.search_position(row_id + 1, 0, visited_tiles)
                else:
                    self.search_position(row_id, col_id + 1, visited_tiles)

                # Exiting recursion, remove the ID from visited_tiles
                visited_tiles.remove(tile.id)


def main():
    input_file = read_input_batch("2020/20/input.txt")
    monster_file = read_input("2020/20/monster.txt", line_strip=False)
    #  Preprocess inputs
    id_list = [int(tile[1][:-1]) for tile in input_file]
    tile_list = [tile[2:] for tile in input_file]

    # Convert characters to 1 and 0, and to array
    X_ids = np.array(id_list, dtype=int)
    X_tiles = np.array(
        [
            [[1 if char == TILE_CHAR else 0 for char in line] for line in tile]
            for tile in tile_list
        ],
        dtype=int,
    )
    X_monster = np.array(
        [[1 if char == TILE_CHAR else 0 for char in line] for line in monster_file],
        dtype=int,
    )
    # Create map object
    mapmap = Map(X_ids, X_tiles)
    # Return result
    print(f"Result of part 1: {np.prod(mapmap.corners)}")
    # Find the correct orientation of the map when looking for sea monsters
    # The correct orientation should exhibit maximum overlap with the monster template
    # (in more than one spot, possibly)
    map_rot_and_flip = rotate_and_flip(mapmap.map)
    correlation_array = np.array(
        [
            correlate2d(map_candidate, X_monster, mode="same")
            for map_candidate in map_rot_and_flip
        ]
    )
    idx_match = np.argmax(np.max(correlation_array, axis=(1, 2)))
    # Find the number of monsters by counting the spots of maximum overlap
    num_monsters = (correlation_array[idx_match] == np.max(correlation_array)).sum()
    # Obtain sea roughness by removing num_monster * sum(monster) values from map
    print(
        "Result of part 2: "
        f"{map_rot_and_flip[idx_match].sum() - num_monsters*X_monster.sum()}"
    )


if __name__ == "__main__":
    main()
