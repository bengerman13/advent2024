from dataclasses import dataclass

from part2.heading import Heading


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
        return all(
            (
                any((self.x < other.x, self.y < other.y)),
                self.x <= other.x,
                self.y <= other.y,
            )
        )

    def __le__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all((self.x <= other.x, self.y <= other.y))

    def __gt__(self, other) -> bool:
        if not isinstance(other, Point):
            raise TypeError("Can't add these types")
        return all(
            (
                any((self.x > other.x, self.y > other.y)),
                self.x >= other.x,
                self.y >= other.y,
            )
        )

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
