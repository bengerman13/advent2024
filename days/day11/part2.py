import sys
from functools import cache


@cache
def blink(number) -> list[int]:
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        return split_int(number)
    else:
        return [number * 2024]


@cache
def split_int(num: int) -> list[int]:
    num_str = str(num)
    half = len(num_str) // 2
    left, right = num_str[:half], num_str[half:]
    return [int(left), int(right)]


@cache
def blink_n_times(stone: int, times: int):
    if times == 0:
        return 1
    else:
        stones = blink(stone)
        times -= 1
        return sum(
            [blink_n_times(stone, times) for stone in stones if stone is not None]
        )


def main():
    with open(sys.argv[1]) as f:
        stones_str = f.readline()
        blinks_str = f.readline()

    stones = [int(x) for x in stones_str.split(" ")]
    blinks = int(blinks_str)
    count = 0
    for stone in stones:
        count += blink_n_times(stone, blinks)
    print(count)


if __name__ == "__main__":
    main()
