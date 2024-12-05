import sys

import dataclasses

KEY_WORD = "XMAS"


@dataclasses.dataclass
class Direction:
    """
    Direction is the angle of a vector
    """

    x: int
    y: int


class Board:
    directions = []
    for x in (-1, 0, 1):
        for y in (-1, 0, 1):
            if not all((x == 0, y == 0)):  # 0,0 doesn't go anywhere.
                directions.append(Direction(x, y))

    def __init__(self, lines: list[list[str]]):
        self.board = lines

    def count_all_matches(self) -> int:
        total = 0
        # walk the board, find all the Xs, then total the XMASes from there
        for y, row in enumerate(self.board):
            for x, letter in enumerate(row):
                if letter == "X":
                    total += self.count_matches_from(x, y)
        return total

    def count_matches_from(self, x, y) -> int:
        """
        Given an X, count the ways it can spell XMAS
        """
        return len(
            [1 for direction in self.directions if self.is_match(x, y, direction)]
        )

    def is_match(self, x: int, y: int, direction: Direction) -> bool:
        """
        Check if a word starting at the given point, along the given Direction, is XMAS
        """
        for letter in KEY_WORD:
            if y < 0 or y >= len(self.board):
                return False
            if x < 0 or x >= len(self.board[y]):
                return False
            if self.board[y][x] != letter:
                return False
            x += direction.x
            y += direction.y

        return True


def main():
    lines: list[list[str]] = []
    with open(sys.argv[1]) as f:
        for l in f.readlines():
            lines.append(l.strip())
    board = Board(lines)
    print(board.count_all_matches())


if __name__ == "__main__":
    main()
