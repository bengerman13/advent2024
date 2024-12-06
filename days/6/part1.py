import sys
from typing import TypeAlias, ClassVar
import dataclasses
import collections


@dataclasses.dataclass
class Heading:
    x: int
    y: int

    def rotate_clockwise(self) -> None:
        if self.y:
            self.y *= -1
        self.y, self.x = self.x, self.y


directions = {
    "V": Heading(0, 1),
    ">": Heading(1, 0),
    "^": Heading(0, -1),
    "<": Heading(-1, 0),
}


@dataclasses.dataclass
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
        if not isinstance(other, Heading):
            raise TypeError("Can't add these types")
        return all((self.x == other.x, self.y == other.y))


@dataclasses.dataclass
class Map:
    grid: list[list[str]]
    lower_right_bound: Point = dataclasses.field(default_factory=lambda: Point(0, 0))
    upper_left_bound: Point = dataclasses.field(default_factory=lambda: Point(0, 0))

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


@dataclasses.dataclass
class Guard:
    location: Point
    heading: Heading

    def walk(self):
        self.location = self.peek()

    def peek(self) -> Point:
        return self.location + self.heading

    def rotate(self):
        self.heading.rotate_clockwise()


class Board:

    def __init__(self) -> None:
        self.map: Map = Map([])
        self.guard: Guard

    def walk_guard_to_end(self) -> int:
        seen = 1
        next_point = self.guard.peek()
        while (
            next_point <= self.map.lower_right_bound
            and next_point >= self.map.upper_left_bound
        ):
            next_char = self.map[next_point]
            if next_char == "#":
                self.guard.rotate()
            elif next_char == ".":
                self.map[next_point] = "X"
                seen += 1
                self.guard.walk()
            elif next_char == "X":
                self.guard.walk()
            next_point = self.guard.peek()
        return seen

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
                            board.guard = Guard(p, directions[char])
                            board.map[p] = "X"
                        else:
                            board.map[p] = char
            board.map.lower_right_bound = p
        return board


def main():
    board = Board.from_file(sys.argv[1])
    print(board.walk_guard_to_end())


if __name__ == "__main__":
    main()
