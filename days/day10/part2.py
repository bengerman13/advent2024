from dataclasses import dataclass, field
import sys


@dataclass(order=True, frozen=True)
class Coord:
    x: int
    y: int

    @property
    def north(self) -> "Coord":
        return Coord(self.x, self.y - 1)

    @property
    def south(self) -> "Coord":
        return Coord(self.x, self.y + 1)

    @property
    def east(self) -> "Coord":
        return Coord(self.x + 1, self.y)

    @property
    def west(self) -> "Coord":
        return Coord(self.x - 1, self.y)

    @property
    def neighbors(self) -> tuple["Coord", "Coord", "Coord", "Coord"]:
        return self.north, self.south, self.east, self.west


@dataclass(frozen=True)
class Tile:
    coord: Coord
    elev: int

    @property
    def y(self):
        return self.coord.y

    @property
    def x(self):
        return self.coord.x


@dataclass
class VolcanoMap:
    tiles: list[list[Tile]] = field(default_factory=list)

    def contains(self, coord: Coord | Tile) -> bool:
        return all(
            (
                coord.y >= 0,
                coord.y < len(self.tiles),
                coord.x >= 0,
                coord.x < len(self.tiles[0]),
            )
        )

    def __getitem__(self, coord: Coord) -> Tile:
        return self.tiles[coord.y][coord.x]


class TrailTrie:

    def __init__(self, coord: Coord, volcano_map: VolcanoMap) -> None:
        self.coord = coord
        self.volcano_map = volcano_map
        self.tile = self.volcano_map[coord]
        self.next_steps = self.walk()
        self._all_steps = set([coord])

    def walk(self) -> list["TrailTrie"]:
        next_steps = []
        for neighbor in self.coord.neighbors:
            if self.volcano_map.contains(neighbor):
                ntile = self.volcano_map[neighbor]
                if ntile.elev - 1 == self.tile.elev:
                    next_steps.append(TrailTrie(neighbor, self.volcano_map))
        return next_steps

    @property
    def all_steps(self) -> set[Coord]:
        if len(self._all_steps) == 1:
            steps = set([self.coord])
            for step in self.next_steps:
                self._all_steps.update(step.all_steps)
        return self._all_steps

    @property
    def score(self):
        return self.distinct_paths_to_nine()

    def distinct_paths_to_nine(self):
        if self.tile.elev == 9:
            return 1
        return sum([step.distinct_paths_to_nine() for step in self.next_steps])

    def __str__(self):
        s = ""
        for row in self.volcano_map.tiles:
            for tile in row:
                if tile.coord in self.all_steps:
                    s += str(tile.elev)
                else:
                    s += "."
            s += "\n"
        return s


def main() -> None:
    volcano_map: VolcanoMap = VolcanoMap()
    trailhead_coords: list[Coord] = []
    trailheads: list[TrailTrie] = []
    with open(sys.argv[1]) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            for x, char in enumerate(line):
                elev = int(char)
                coord = Coord(x=x, y=y)
                tile = Tile(coord, elev)
                if y == len(volcano_map.tiles):
                    volcano_map.tiles.append([])
                volcano_map.tiles[coord.y].append(tile)
                if elev == 0:
                    trailhead_coords.append(coord)
    for trailhead_coord in trailhead_coords:
        trailheads.append(TrailTrie(trailhead_coord, volcano_map))
    total = 0
    for trailhead in trailheads:
        # print(str(trailhead))
        # print(trailhead.score)
        total += trailhead.score
    print(total)


if __name__ == "__main__":
    main()
