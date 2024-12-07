import sys
from functools import cache
from dataclasses import dataclass
from collections import deque

@dataclass
class Equation:
    answer: int
    inputs: deque[int]

    @classmethod
    def from_string(cls, string: str) -> 'Equation':
        answer_str, inputs_str = string.split(": ")
        answer = int(answer_str)
        inputs = deque([int(x) for x in inputs_str.split(" ")])
        return cls(answer, inputs)

    def can_solve(self):
        return can_solve(self.answer, *self.inputs)


@cache
def can_solve(answer: int, *args) -> bool:
    if len(args) == 1:
        return args[0] == answer
    added = args[0] + args[1]
    multiplied = args[0] * args[1]
    concatenated = int(f"{args[0]}{args[1]}")
    return can_solve(answer, *[added, *args[2:]]) or can_solve(answer, *[multiplied, *args[2:]]) or can_solve(answer, *[concatenated, *args[2:]])


def main():
    with open(sys.argv[1]) as f:
        equation_strs = [line.strip() for line in f.readlines()] 
    equations = [Equation.from_string(e) for e in equation_strs]
    solvable = [e for e in equations if e.can_solve()]
    print(sum([e.answer for e in solvable]))
    

if __name__ == "__main__":
    main()
