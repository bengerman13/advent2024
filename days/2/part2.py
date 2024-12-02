#!/usr/bin/env python3

import sys


def sign(num):
    return -1 if num < 0 else 1


def list_without(l: list, i: int) -> list:
    l2 = [x for x in l]
    del l2[i]
    return l2


class Report:
    def __init__(self, input_: str) -> None:
        self.levels = [int(i) for i in input_.split(" ")]

    def is_safe(self) -> bool:
        def is_list_safe(levels) -> bool:
            last_delta = 0
            for i in range(len(levels) - 1):
                delta = levels[i + 1] - levels[i]
                if i == 0:
                    last_delta = delta
                if sign(last_delta) != sign(delta):
                    return False
                if abs(delta) not in (1, 2, 3):
                    return False
                last_delta = delta

            return True

        if is_list_safe(self.levels):
            return True
        for skip in range(len(self.levels)):
            if is_list_safe(list_without(self.levels, skip)):
                return True
        return False


def main():
    with open(sys.argv[1]) as f:
        reports = [Report(line.strip()) for line in f.readlines()]
    safe_reports = [report for report in reports if report.is_safe()]
    print(len(safe_reports))


if __name__ == "__main__":
    main()
