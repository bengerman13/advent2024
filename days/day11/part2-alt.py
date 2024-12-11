# this solution didn't work, but it's clever so I'm hanging on to it :D
import sys
from dataclasses import dataclass, field
from typing import Optional
from functools import cache
import datetime


@dataclass
class LinkedStone:

    number: int
    blinks_left: int
    next_stone: Optional["LinkedStone"]
    head: "LinkedStone" = Optional["LinkedStone"]

    def blink(self) -> "LinkedStone":
        self.blinks_left -= 1
        current_next = self.next_stone
        a, b = blink(self.number)
        self.number = a
        if b is not None:
            new_next = LinkedStone(b, self.blinks_left, current_next, self.head)
            self.next_stone = new_next
        return current_next

    def pop_head(self):
        old_head = self.head
        head = old_head.next_stone
        stone = head
        while (stone := stone.next_stone) is not None:
            stone.head = head
        return old_head

    def __str__(self) -> str:
        return f"{self.number}, {str(self.next_stone)}"

    def __len__(self) -> int:
        total = 1
        stone = self.head
        while (stone := stone.next_stone) is not None:
            total += 1
        return total

    def append(self, other: "LinkedStone") -> "LinkedStone":
        last = self.head
        while (last := last.next_stone) is not None:
            pass
        last.next_stone = other
        while (last := last.next_stone) is not None:
            last.head = self.head


@cache
def blink(number):
    if number == 0:
        return (1, None)
    elif len(str(number)) % 2 == 0:
        return split_int(number)
    else:
        return (number * 2024, None)


@cache
def split_int(num: int) -> tuple[int, int]:
    num_str = str(num)
    half = len(num_str) // 2
    left, right = num_str[:half], num_str[half:]
    return int(left), int(right)


def blink_n_times(stone_head):
    count = 0
    while stone_head is not None:
        count += 1
        while stone_head.blinks_left > 0:
            stone_head.blink()
        old_head = stone_head.pop_head()
        stone_head = stone_head.next_stone

    return count


def main():
    with open(sys.argv[1]) as f:
        stones_str = f.readline()
        blinks_str = f.readline()

    stones = [int(x) for x in stones_str.split(" ")]
    blinks = int(blinks_str)
    total = 0
    for stone in reversed(stones):
        linked_stone = LinkedStone(stone, blinks, None)
        linked_stone.head = linked_stone
        total += blink_n_times(linked_stone)

    print(total)


if __name__ == "__main__":
    main()
