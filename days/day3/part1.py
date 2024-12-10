import re
import sys
from dataclasses import dataclass


MUL_FINDER = re.compile(r"(?P<instruction>mul)\((?P<first>\d+),(?P<second>\d+)\)")


@dataclass
class Mul:
    name: str
    x: int
    y: int


def parse_line(line: str) -> list[Mul]:
    ints: list[Mul] = []
    for match in MUL_FINDER.finditer(line):
        d = match.groupdict()
        ints.append(Mul(d["instruction"], int(d["first"]), int(d["second"])))
    return ints


def main() -> None:
    instructions: list[Mul] = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            results = parse_line(line)
            instructions.extend(results)
    total = 0
    for instruction in instructions:
        total += instruction.x * instruction.y
    print(total)


if __name__ == "__main__":
    main()
