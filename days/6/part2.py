import sys
from typing import TypeAlias, ClassVar
from dataclasses import dataclass, field
from collections import deque, defaultdict


@dataclass
class Heading:
    x: int
    y: int

    def rotate_clockwise(self) -> "Heading":
        y = self.y
        x = self.x
        if y:
            y *= -1
        return Heading(y, x)

    def __hash__(self):
        return hash(f"{self.x}{self.y}")


directions = {
    "V": Heading(0, 1),
    ">": Heading(1, 0),
    "^": Heading(0, -1),
    "<": Heading(-1, 0),
}


@dataclass
class Point:
    x: int
    y: int

    def __add__(self, other) -> "Point":
        if not isinstance(other, Heading):
            raise TypeError("Can't add these types")
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x < other.x, self.y < other.y))

    def __le__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x <= other.x, self.y <= other.y))

    def __gt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x > other.x, self.y > other.y))

    def __ge__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x >= other.x, self.y >= other.y))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x == other.x, self.y == other.y))

    def __hash__(self):
        return hash(f"{self.x}{self.y}")


@dataclass
class Map:
    grid: list[list[str]]
    lower_right_bound: Point = field(default_factory=lambda: Point(0, 0))
    upper_left_bound: Point = field(default_factory=lambda: Point(0, 0))
    obstacles: set[Point] = field(default_factory=set)

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
                s += point
            s += "\n"
        return s

    def contains(self, point: Point) -> bool:
        return point <= self.lower_right_bound and point >= self.upper_left_bound


@dataclass
class Vector:
    origin: Point
    heading: Heading

    def next_step(self):
        return self.origin + self.heading

    def points_at(self, target: Point) -> bool:
        if self.heading.x:
            return (
                target.y == self.origin.y
                and ((1 + target.x) * self.heading.x) <= (1 + self.origin.x)
            )
        if self.heading.y:
            return (
                target.x == self.origin.x
                and ((1 + target.y) * self.heading.y) <= (1 + self.origin.y)
            )
        return val

    def rotated(self) -> "Vector":
        return Vector(self.origin, self.heading.rotate_clockwise())


@dataclass
class Guard:
    vector: Vector
    obstacles: set[Point] = field(default_factory=set)
    obstacles_by_heading: defaultdict[Heading, list[Point]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def walk(self) -> str:
        self.vector.origin = self.peek()
        if self.vector.heading.x:
            return "-"
        else:
            return "|"

    def peek(self) -> Point:
        return self.vector.next_step()

    def avoid_obstacle(self):
        next_step = self.peek()
        self.obstacles.add(next_step)
        self.obstacles_by_heading[self.vector.heading].append(next_step)
        self.vector.heading = self.vector.heading.rotate_clockwise()

    def blocking_next_step_would_loop(self, map_: Map) -> bool:
        # first: if we can jump back in a path we already tread in the same direction, that's definitely a loop, righ?
        test_vector = self.vector.rotated()
        for obstacle in self.obstacles_by_heading[test_vector.heading]:
            if test_vector.points_at(obstacle):
                return True

        # second: we might also be able to hit an obstacle from another direction and force a loop
        # but here we just have to walk it and see.
        test_guard = Guard(test_vector)
        for obstacle in map_.obstacles:
            if test_vector.points_at(obstacle):
                if test_guard.check_for_loops(map_):
                    return True
        return False

    def check_for_loops(self, map_: Map) -> bool:
        next_ = self.peek()
        while map_.contains(next_):
            if next_ in self.obstacles:
                return True
            if map_[next_] == "#":
                self.avoid_obstacle()
            self.walk()
            next_ = self.peek()
        return False


class Board:

    def __init__(self) -> None:
        self.map: Map = Map([])
        self.guard: Guard

    def walk_guard_to_end(self) -> tuple[int, int]:
        seen = 1
        potential_boxes = 0
        next_point = self.guard.peek()
        while (
            next_point <= self.map.lower_right_bound
            and next_point >= self.map.upper_left_bound
        ):
            next_char = self.map[next_point]
            if self.guard.blocking_next_step_would_loop(self.map):
                # print("can block here!")
                potential_boxes += 1
                self.map[self.guard.peek()] = "o"
            if next_char == "#":
                self.map[self.guard.vector.origin] = "+"
                self.guard.avoid_obstacle()
            else:
                if next_char == ".":
                    self.map[self.guard.vector.origin] = self.guard.walk()
                    seen += 1
                elif next_char in "-|+X":
                    self.map[self.guard.vector.origin] = self.guard.walk()
                elif next_char == "o":
                    self.guard.walk()
            next_point = self.guard.peek()
        return seen, potential_boxes

    @classmethod
    def from_file(cls, filename: str) -> "Board":
        board = cls()
        with open(filename) as f:
            x = 0
            y = 0
            for y, line in enumerate(f.readlines()):
                line = line.strip()
                if len(line):
                    for x, char in enumerate(line):
                        p = Point(x, y)
                        if char in directions:
                            board.guard = Guard(Vector(p, directions[char]))
                            board.map[p] = "X"
                        else:
                            if char == "#":
                                board.map.obstacles.add(p)
                            board.map[p] = char
            board.map.lower_right_bound = p
        return board


def main():
    board = Board.from_file(sys.argv[1])
    print(board.walk_guard_to_end())


if __name__ == "__main__":
    main()
