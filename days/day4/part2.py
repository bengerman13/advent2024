import sys


class Board:
    def __init__(self, lines: list[list[str]]):
        self.board = lines

    def count_all_matches(self) -> int:
        total = 0
        # walk the board, finding all As
        for y, row in enumerate(self.board):
            for x, letter in enumerate(row):
                if letter == "A":
                    # check if this A is an X-MAS
                    total += self.count_matches_from(x, y)
        return total

    def count_matches_from(self, x, y) -> int:
        if self.is_match(x, y):
            return 1
        return 0

    def is_match(self, x: int, y: int) -> bool:
        # check if we'll stay in bounds
        if any((x < 1, y < 1, y + 1 >= len(self.board), x + 1 >= len(self.board[y]))):
            return False

        negative = []  # letters on the negative slope (\)
        negative.append(self.board[y - 1][x - 1])
        negative.append(self.board[y + 1][x + 1])

        positive = []  # letters on the positive slope (/)
        positive.append(self.board[y - 1][x + 1])
        positive.append(self.board[y + 1][x - 1])
        return sorted(negative) == ["M", "S"] and sorted(positive) == ["M", "S"]


def main():
    lines: list[list[str]] = []
    with open(sys.argv[1]) as f:
        for l in f.readlines():
            lines.append(l.strip())
    board = Board(lines)
    print(board.count_all_matches())


if __name__ == "__main__":
    main()
