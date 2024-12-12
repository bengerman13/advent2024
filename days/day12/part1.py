import sys
from dataclasses import dataclass, field
from typing import Optional

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
class Plant:
    char: str


@dataclass
class Region:
    plant: Plant
    plots: set['Plot'] = field(default_factory=set)
    
    @classmethod
    def from_plot(cls, plot: 'Plot'):
        region = cls(plant=plot.plant)
        region.flood_fill_from_plot(plot)
        return region

    def flood_fill_from_plot(self, plot: 'Plot'):
        # TODO: do we need to worry about merging 
        # neighboring plots?
        if plot in self:
            return
        if plot.plant == self.plant:
            self.plots.add(plot)
            plot.region = self
            for nplot in plot.neighbors:
                self.flood_fill_from_plot(nplot)

    @property
    def area(self) -> int:
        return len(self.plots)

    @property
    def perimeter(self):
        return sum([plot.fences for plot in self.plots])

    @property
    def fence_cost(self) -> int:
        return self.area * self.perimeter

    def __contains__(self, plot: 'Plot'):
        return plot in self.plots

    def print(self, grid):
        s = ""
        for row in grid.tiles:
            for plot in row:
                if plot in self:
                    s += self.plant.char
                else:
                    s += "."
            s += "\n"
        print(s)

        
@dataclass(unsafe_hash=True)
class Plot:
    plant: Plant
    coord: Coord
    grid: 'Grid' = field(compare=False, repr=False)
    region: Optional[Region] = field(compare=False, default=None)

    @property
    def neighbors(self):
        return [self.grid[neighbor] for neighbor in self.coord.neighbors if neighbor in self.grid]

    @property
    def fences(self):
        fences = 4
        for neighbor in self.neighbors:
            #print(f"{self=}, {neighbor=}")
            if neighbor in self.region:
                fences -= 1
        return fences

@dataclass
class Grid:
    tiles: list[list['Plot']] = field(default_factory=list)
    regions: dict[Plant, list[Region]] = field(default_factory=dict)

    @property
    def height(self) -> int:
        return len(self.tiles)

    @property
    def width(self) -> int:
        return len(self.tiles[0])

    def __getitem__(self, coord: Coord):
        return self.tiles[coord.y][coord.x]
    
    def __contains__(self, coord: Coord):
        return all((coord.y >= 0, coord.y < self.height, coord.x >= 0, coord.x < self.width))


def main():
    farm = Grid()
    with open(sys.argv[1]) as f:
        for y, line in enumerate(f.readlines()):
            line = line.strip()
            farm.tiles.append([])
            for x, plant_id in enumerate(line):
                plot = Plot(Plant(plant_id), Coord(x, y), farm)
                farm.tiles[y].append(plot)

    for row in farm.tiles:
        for plot in row:
            if plot.region is None:
                region = Region.from_plot(plot)
                farm.regions[region.plant] = farm.regions.get(region.plant, [])
                farm.regions[region.plant].append(region)
    
    total = 0
    for plant, regions in farm.regions.items():
        for region in regions:
            region.print(farm)
            total += region.fence_cost
    print(total)


if __name__ == "__main__":
    main()
