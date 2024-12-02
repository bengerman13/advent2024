#!/usr/bin/env python3

from typing import TextIO

from itertools import zip_longest
import sys


def get_lists(raw: TextIO) -> tuple[list[int], list[int]]:
    sep = "   "
    left = []
    right = []
    for line in raw.readlines():
        l, _, r = line.strip().partition(sep)
        left.append(int(l))
        right.append(int(r))
    return left, right


def compare_lists(left, right) -> int:
    total = 0
    for l, r in zip_longest(left, right):
        total += abs(l - r)
    return total


def sort_list(ls: list) -> list:
    return sorted(ls)


def main():
    with open(sys.argv[1]) as f:
        left, right = get_lists(f)
    print(compare_lists(sort_list(left), sort_list(right)))


if __name__ == "__main__":
    main()
