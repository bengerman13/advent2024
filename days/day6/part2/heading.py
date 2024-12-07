from dataclasses import dataclass


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


NORTH = Heading(0, -1)
SOUTH = Heading(0, 1)
EAST = Heading(1, 0)
WEST = Heading(-1, 0)
