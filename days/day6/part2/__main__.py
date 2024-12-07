import sys
from typing import TypeAlias, ClassVar
from dataclasses import dataclass, field
from collections import deque, defaultdict

from part2.point import Point
from part2.heading import Heading
from part2.vector import Vector
from part2.floor_map import FloorMap, FloorTile


def main():
    with open(sys.argv[1]) as f:
        contents = "".join(f.readlines())
    floor_map = FloorMap.from_str(contents)
    potential_obstacles = 0
    floor_map.walk_guard_to_end()
    for y, row in enumerate(floor_map.grid):
        for x, tile in enumerate(row):
            if not any((tile.is_guard_starting_point, tile.is_obstacle)):
                if tile in floor_map.visited_tiles:
                    test_map = FloorMap.from_str(contents)
                    test_map.grid[y][x].is_test_obstacle = True
                    if test_map.walk_guard_to_end_and_check_for_loops():
                        potential_obstacles += 1
    print(len(floor_map.visited_tiles))
    print(potential_obstacles)


if __name__ == "__main__":
    main()
