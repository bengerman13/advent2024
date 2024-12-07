import copy
from dataclasses import dataclass, field
import itertools

from part2.vector import Vector
from part2.point import Point
from part2 import heading


directions_for_str = {
    "V": heading.SOUTH,
    ">": heading.EAST,
    "^": heading.NORTH,
    "<": heading.WEST,
}

str_for_directions = {
    heading.SOUTH: "V",
    heading.EAST: ">",
    heading.NORTH: "^",
    heading.WEST: "<",
}


class RevisitException(BaseException):
    pass


class ObstacleBlockingException(BaseException):
    pass


@dataclass
class FloorTile:
    location: Point
    visited_directions: set[heading.Heading] = field(default_factory=set)
    is_obstacle: bool = False
    is_test_obstacle: bool = False
    guard: Vector | None = None
    is_guard_starting_point: bool = False

    def __str__(self):
        if self.guard is not None:
            return str_for_directions[self.guard.heading]
        if self.is_obstacle:
            return "#"
        if self.is_test_obstacle:
            return "o"
        if not len(self.visited_directions):
            return "."
        ns = (
            heading.NORTH in self.visited_directions
            or heading.SOUTH in self.visited_directions
        )
        ew = (
            heading.EAST in self.visited_directions
            or heading.WEST in self.visited_directions
        )
        if ns:
            if ew:
                return "+"
            return "|"
        if ew:
            return "-"
        return "?"

    def visit(self, guard: Vector):
        if len(self.visited_directions):
            is_first_visit = False
        if self.is_obstacle or self.is_test_obstacle:
            raise ObstacleBlockingException()
        if guard.heading in self.visited_directions:
            raise RevisitException()
        self.guard = guard
        self.visited_directions.add(guard.heading)

    def leave(self) -> None:
        self.guard = None

    @property
    def visited(self) -> bool:
        return bool(len(self.visited_directions))

    def __hash__(self):
        return hash(self.location)

    @classmethod
    def from_str(cls, symbol: str, location: Point) -> "FloorTile":
        this = cls(location)
        if symbol == "#":
            this.is_obstacle = True
        elif symbol in directions_for_str:
            direction = directions_for_str[symbol]
            this.visited_directions.add(direction)
            this.guard = Vector(this.location, direction)
        return this


@dataclass
class FloorMap:
    grid: list[list[FloorTile]]
    guard: Vector
    lower_right_bound: Point = field(default_factory=lambda: Point(0, 0))
    upper_left_bound: Point = field(default_factory=lambda: Point(0, 0))
    obstacles: set[FloorTile] = field(default_factory=set)
    potential_loop_obstacles: set[FloorTile] = field(default_factory=set)
    tested_loop_obstacle_vectors: set[Vector] = field(default_factory=set)

    @property
    def size(self) -> int:
        return len(self.grid) * len(self.grid[0])

    def __getitem__(self, point: Point) -> str:
        return self.grid[point.y][point.x]

    def __setitem__(self, point: Point, val: str) -> None:
        if point.y >= len(self.grid):
            self.grid.append([])
        if point.x == len(self.grid[point.y]):
            self.grid[point.y].append(val)
        else:
            self.grid[point.y][point.x] = val

    def __str__(self) -> str:
        s = ""
        for line in self.grid:
            for point in line:
                s += str(point)
            s += "\n"
        return s

    @classmethod
    def from_str(cls, blob: str) -> "FloorMap":
        tiles: list[list[FloorTile]] = []
        obstacles = set()

        for y, line in enumerate(blob.split("\n")):
            line = line.strip()
            if len(line):
                row = []
                tiles.append(row)
                for x, char in enumerate(line):
                    p = Point(x, y)
                    tile = FloorTile.from_str(char, p)
                    if tile.guard is not None:
                        guard = tile.guard
                    elif tile.is_obstacle:
                        obstacles.add(tile)
                    row.append(tile)

        board = cls(tiles, guard, lower_right_bound=p, obstacles=obstacles)
        return board

    def advance_guard(self) -> None:
        this_tile = self.guard.origin
        next_tile = self.guard.next_step()
        if not self.contains(next_tile):
            raise IndexError()
        try:
            self[next_tile].visit(self.guard)
            self.guard = Vector(next_tile, self.guard.heading)
            self[this_tile].leave()
        except ObstacleBlockingException:
            self.guard = self.guard.rotated()
            # visit this tile again so it knows it's been visited from 2 directions
            self[this_tile].visit(self.guard)
        # print(str(self))

    def walk_guard_to_end(self) -> None:
        while True:
            try:
                # if self.blank_clone().would_loop_ahead():
                #    print("found one")
                #    self.potential_loop_obstacles.add(self.guard.next_step())
                # self.tested_loop_obstacle_vectors.add(self.guard)
                self.advance_guard()
            except IndexError:
                return

    def would_loop_ahead(self) -> bool:
        next_step = self[self.guard.next_step()]
        if self.guard in self.tested_loop_obstacle_vectors:
            # print(f"{self.guard=}, {self.tested_loop_obstacle_vectors=}")
            return False
        if next_step.is_obstacle:
            return False
        next_step.is_test_obstacle = True
        return self.walk_guard_to_end_and_check_for_loops()

    def walk_guard_to_end_and_check_for_loops(self) -> bool:
        steps = 0
        size = self.size
        while steps <= size:
            try:
                # print(self)
                self.advance_guard()
            except IndexError:
                return False
            except RevisitException:
                return True
            steps += 1
        print("size exceeded!")

    def blank_clone(self) -> "FloorMap":
        clone = copy.deepcopy(self)
        return clone

    def contains(self, point: Point) -> bool:
        return point <= self.lower_right_bound and point >= self.upper_left_bound

    @property
    def visited_tiles(self) -> list[FloorTile]:
        return [tile for tile in itertools.chain(*self.grid) if tile.visited]
