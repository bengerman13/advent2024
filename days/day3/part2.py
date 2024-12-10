import re
import sys
from dataclasses import dataclass
from typing import TypeAlias

PARSER = re.compile(
    r"((?P<instruction>mul)\((?P<first>\d+),(?P<second>\d+)\))|(?P<do>do\(\))|(?P<donot>don't\(\))"
)


@dataclass
class State:
    enabled: bool = True
    total: int = 0


@dataclass
class Toggle:
    polarity: bool

    def apply(self, state: State) -> None:
        state.enabled = self.polarity


@dataclass
class Mul:
    name: str
    x: int
    y: int

    def apply(self, state: State):
        if state.enabled:
            state.total += self.x * self.y


Instruction: TypeAlias = Toggle | Mul

DONOT = Toggle(False)
DO = Toggle(True)


def parse_line(line) -> list[Instruction]:
    program: list[Instruction] = []
    for match in PARSER.finditer(line):
        d = match.groupdict()
        if d["instruction"]:
            program.append(Mul(d["instruction"], int(d["first"]), int(d["second"])))
        elif d["do"]:
            program.append(DO)
        elif d["donot"]:
            program.append(DONOT)
    return program


def run_program(program: list[Instruction]) -> int:
    state = State()
    for instruction in program:
        instruction.apply(state)
    return state.total


def main() -> None:
    instructions: list[Instruction] = []
    with open(sys.argv[1]) as f:
        for line in f.readlines():
            results = parse_line(line)
            instructions.extend(results)
    total = run_program(instructions)
    print(total)


if __name__ == "__main__":
    main()
