from collections import defaultdict
from dataclasses import dataclass, field
import sys


@dataclass
class Point:
    x: int
    y: int
    is_antinode: bool = False
    antenna_frequency: str | None = None

    def __add__(self, other: "Delta") -> "Point":
        if not isinstance(other, Delta):
            raise TypeError("Can't add these types")
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Delta":
        if isinstance(other, Point):
            return Delta(self.x - other.x, self.y - other.y)
        if isinstance(other, Delta):
            return Point(self.x - other.x, self.y - other.y)
        raise TypeError("Can't subtract these types")

    def __lt__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't compare these types")
        return all(
            (
                any((self.x < other.x, self.y < other.y)),
                self.x <= other.x,
                self.y <= other.y,
            )
        )

    def __le__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't compare these types")
        return all((self.x <= other.x, self.y <= other.y))

    def __gt__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't compare these types")
        return all(
            (
                any((self.x > other.x, self.y > other.y)),
                self.x >= other.x,
                self.y >= other.y,
            )
        )

    def __ge__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't compare these types")
        return all((self.x >= other.x, self.y >= other.y))

    def __eq__(self, other: "Point") -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't compare these types")
        return all((self.x == other.x, self.y == other.y))

    def __hash__(self):
        return hash(f"{self.x}{self.y}")

    def __str__(self):
        if self.antenna_frequency is not None:
            return self.antenna_frequency
        elif self.is_antinode:
            return "#"
        else:
            return "."

    @classmethod
    def from_str(cls, x: int, y: int, char: str) -> "Point":
        if char == ".":
            char = None
        return cls(x=x, y=y, antenna_frequency=char)


@dataclass
class Delta:
    x: int
    y: int


@dataclass
class Grid:
    grid: list[list[Point]] = field(default_factory=list)

    @property
    def upper(self):
        return self.grid[-1][-1]

    @property
    def lower(self):
        return self.grid[0][0]

    def contains(self, point: Point) -> bool:
        return point <= self.upper and point >= self.lower

    def __str__(self):
        blob: str = ""
        for row in self.grid:
            for point in row:
                blob += str(point)
            blob += "\n"
        return blob

    def __getitem__(self, point: Point) -> Point:
        return self.grid[point.y][point.x]

    def __setitem__(self, point: Point, val: Point) -> None:
        if point.y >= len(self.grid):
            self.grid.append([])
        if point.x == len(self.grid[point.y]):
            self.grid[point.y].append(val)
        else:
            self.grid[point.y][point.x] = val


def find_antinodes(a: Point, b: Point, grid: Grid) -> list[Point]:
    antinodes = []
    delta = a - b
    next_antinode = a + delta
    while grid.contains(next_antinode):
        antinodes.append(next_antinode)
        next_antinode += delta
    next_antinode = b - delta
    while grid.contains(next_antinode):
        antinodes.append(next_antinode)
        next_antinode -= delta
    antinodes.append(a)
    antinodes.append(b)
    return antinodes


def main():

    grid = Grid()
    antennas_by_frequency: defaultdict[str, list[Point]] = defaultdict(list)
    antinodes: set[Point] = set()

    with open(sys.argv[1]) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, char in enumerate(line):
                point = Point.from_str(x, y, char)
                grid[point] = point
                if point.antenna_frequency is not None:
                    antennas_by_frequency[point.antenna_frequency].append(point)

    for frequency, antennas in antennas_by_frequency.items():
        if len(antennas) > 1:
            for ithis, this in enumerate(antennas):
                for iother, other in enumerate(antennas):
                    if ithis == iother:
                        continue
                    else:
                        nodes = find_antinodes(this, other, grid)
                        for node in nodes:
                            grid[node].is_antinode = True
                            antinodes.add(node)
    print(grid)
    print(len(antinodes))


if __name__ == "__main__":
    main()
