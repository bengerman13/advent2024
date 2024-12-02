#!/usr/bin/env python3

from typing import TextIO

from itertools import zip_longest
import sys


def get_lists(raw: TextIO) -> tuple[dict[int, int], dict[int, int]]:
    sep = "   "
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    for line in raw.readlines():
        lstr, _, rstr = line.strip().partition(sep)
        l = int(lstr)
        r = int(rstr)
        left_count = left.get(l, 0)
        left[l] = left_count + 1
        right_count = right.get(r, 0)
        right[r] = right_count + 1
    return left, right


def compare_lists(left: dict[int, int], right: dict[int, int]) -> int:
    total = 0
    for number, count in left.items():
        similarity = number * count * right.get(number, 0)
        print(f"{number=}, {count=}, {similarity=}")
        total += similarity
    return total


def sort_list(ls: list) -> list:
    return sorted(ls)


def main():
    with open(sys.argv[1]) as f:
        left, right = get_lists(f)
    print(compare_lists(left, right))


if __name__ == "__main__":
    main()
