import sys
from dataclasses import dataclass, field
from typing import Optional
import itertools


@dataclass(order=True, frozen=True)
class Heading:
    x: int
    y: int


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

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        return Heading(x=x, y=y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Coord(x=x, y=y)


@dataclass(frozen=True, order=True)
class Vector:
    origin: Coord
    heading: Heading


@dataclass(frozen=True)
class Plant:
    char: str


@dataclass
class Region:
    plant: Plant
    plots: set["Plot"] = field(default_factory=set)

    @classmethod
    def from_plot(cls, plot: "Plot"):
        region = cls(plant=plot.plant)
        region.flood_fill_from_plot(plot)
        return region

    def flood_fill_from_plot(self, plot: "Plot"):
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
        return sum([plot.num_fences for plot in self.plots])

    def perimeter_plots(self):
        return [plot for plot in self.plots if plot.num_fences > 0]

    def count_sides(self):
        def process_fences_by_heading(fences_: list[Vector], heading: Heading) -> int:
            """
            find the number of sides facing a given direction
            """

            sides = 0
            if heading.x:
                filter_function = lambda x: x.origin.x
            elif heading.y:
                filter_function = lambda x: x.origin.y

            fences_.sort(key=filter_function)

            for row_column, fence_group in itertools.groupby(fences_, filter_function):
                group = list(fence_group)
                print(f"{row_column=}, {heading=}, {group=}")
                sides += process_fences_by_row_column(fences_=group, heading=heading)
            return sides

        def process_fences_by_row_column(
            fences_: list[Vector], heading: Heading
        ) -> int:
            """
            find the number of sides facing a given direction and perpendicular line
            """
            if heading.x:
                pos = lambda x: x.origin.y
            elif heading.y:
                pos = lambda x: x.origin.x
            fences_.sort(key=pos)
            last_pos = -1
            run_starts = list()
            for fence in fences_:
                print(f"\t\t{fence=}")
                this_pos = pos(fence)
                if last_pos == -1:
                    # prime the loop
                    last_pos = this_pos
                    run_starts.append(last_pos)
                    continue
                if abs(this_pos - last_pos) != 1:
                    run_starts.append(this_pos)
                last_pos = this_pos
            print(f"\t{run_starts=}")
            return len(run_starts)

        fences = []
        direction = None
        for plot in self.perimeter_plots():
            for fence in plot.fences:
                fences.append(fence)
        fences = sorted(fences, key=lambda x: x.heading)
        sides = 0
        for heading, group in itertools.groupby(fences, lambda x: x.heading):
            fence_group = list(group)
            sides += process_fences_by_heading(fence_group, heading)
        print(f"{sides=}")
        return sides

    @property
    def fence_cost(self) -> int:
        return self.area * self.perimeter

    @property
    def fence_cost_discount(self) -> int:
        return self.area * self.count_sides()

    def __contains__(self, plot: "Plot"):
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
    grid: "Grid" = field(compare=False, repr=False)
    region: Optional[Region] = field(compare=False, default=None)

    @property
    def neighbors(self):
        return [
            self.grid[neighbor]
            for neighbor in self.coord.neighbors
            if neighbor in self.grid
        ]

    @property
    def region_neighbors(self):
        return [n for n in self.neighbors if n.plant == self.plant]

    @property
    def non_region_neighbors(self):
        return [
            n
            for n in self.coord.neighbors
            if n not in self.grid or self.grid[n].plant != self.plant
        ]

    @property
    def num_fences(self):
        fences = 4
        for neighbor in self.neighbors:
            # print(f"{self=}, {neighbor=}")
            if neighbor in self.region:
                fences -= 1
        return fences

    @property
    def fences(self):
        fences = []
        for neighbor in self.non_region_neighbors:
            heading = neighbor - self.coord
            fences.append(Vector(self.coord, heading))
        return fences


@dataclass
class Grid:
    tiles: list[list["Plot"]] = field(default_factory=list)
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
        return all(
            (coord.y >= 0, coord.y < self.height, coord.x >= 0, coord.x < self.width)
        )


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

    total_old = 0
    total_discount = 0
    for plant, regions in farm.regions.items():
        for region in regions:
            region.print(farm)
            discount_cost = region.fence_cost_discount
            # print(f"{region.fence_cost=}")
            print(f"{discount_cost=}")
            total_old += region.fence_cost
            total_discount += discount_cost
    print(f"{total_old=}, {total_discount=}")


if __name__ == "__main__":
    main()
