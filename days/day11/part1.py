import sys


def split_int(num: int) -> tuple[int, int]:
    num_str = str(num)
    half = len(num_str) // 2
    left, right = num_str[:half], num_str[half:]
    return int(left), int(right)


def blink_one_stone(stone: int) -> list[int]:
    # process a rule on a stone, return a list with the resulting stone(s)
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        return [*split_int(stone)]
    else:
        return [stone * 2024]


def blink_all(stones: list[int]) -> list[int]:
    i = 0
    while i < len(stones):
        new = blink_one_stone(stones[i])
        stones = [*stones[:i], *new, *stones[i + 1 :]]
        i += len(new)
    return stones


def main():
    with open(sys.argv[1]) as f:
        stones_str = f.readline()
        blinks_str = f.readline()
    stones = [int(x) for x in stones_str.split(" ")]
    blinks = int(blinks_str)
    for _ in range(blinks):
        stones = blink_all(stones)
        print(stones)
    print(len(stones))


if __name__ == "__main__":
    main()
