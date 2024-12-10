from dataclasses import dataclass, field
import itertools
import sys


@dataclass
class Block:
    file_id: int | None

    @property
    def is_free(self) -> bool:
        return self.file_id is None

    def __str__(self) -> str:
        if self.file_id is not None:
            return str(self.file_id)
        return "."


@dataclass
class Disk:
    blocks: list = field(default_factory=list)

    def walk(self):
        empty_seeker = 0
        file_seeker = len(self.blocks) - 1
        while empty_seeker < file_seeker:
            while not self.blocks[empty_seeker].is_free:
                empty_seeker += 1
            while self.blocks[file_seeker].is_free:
                file_seeker -= 1
            if empty_seeker < file_seeker:
                self.swap(empty_seeker, file_seeker)
            # print(self)

    def swap(self, left_idx: int, right_idx: int) -> None:
        self.blocks[left_idx], self.blocks[right_idx] = (
            self.blocks[right_idx],
            self.blocks[left_idx],
        )

    @property
    def checksum(self) -> int:
        cs = 0
        for x, block in enumerate(self.blocks):
            if block.file_id is not None:
                cs += x * block.file_id
        return cs

    @classmethod
    def from_str(cls, rep: str) -> "Disk":
        blocks: list[Block] = []
        for x, pair in enumerate(itertools.batched(rep, 2)):
            if len(pair) == 1:
                file_blocks_str = pair[0]
                empty_blocks_str = "0"
            else:
                file_blocks_str, empty_blocks_str = pair

            file_blocks = int(file_blocks_str)
            empty_blocks = int(empty_blocks_str)
            for _ in range(file_blocks):
                blocks.append(Block(x))
            for _ in range(empty_blocks):
                blocks.append(Block(None))
        return cls(blocks)

    def __str__(self) -> str:
        return "".join([str(block) for block in self.blocks])


def main():
    with open(sys.argv[1]) as f:
        line = f.readline()
    line = line.strip()
    disk = Disk.from_str(line)
    print(disk)
    disk.walk()
    print(disk)
    print(disk.checksum)


if __name__ == "__main__":
    main()
