from dataclasses import dataclass

from part2.point import Point
from part2.heading import Heading


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
                and (target.x - self.origin.x) * self.heading.x >= 0
            )
        if self.heading.y:
            return (
                target.x == self.origin.x
                and (target.y - self.origin.y) * self.heading.y >= 0
            )
        return val

    def rotate(self) -> "Vector":
        self.heading = self.heading.rotate_clockwise()

    def rotated(self) -> "Vector":
        return Vector(
            Point(self.origin.x, self.origin.y), self.heading.rotate_clockwise()
        )

    def __hash__(self):
        return hash(f"{self.origin.x}{self.origin.y}{self.heading.x}{self.heading.y}")
