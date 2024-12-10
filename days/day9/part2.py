from dataclasses import dataclass, field
import itertools
import sys

import traceback


@dataclass
class Block:
    file_id: int | None
    run_start: int
    run_end: int

    @property
    def run_length(self):
        return self.run_end - self.run_start + 1

    @property
    def is_free(self) -> bool:
        return self.file_id is None

    def __str__(self) -> str:
        if self.file_id is not None:
            return str(self.file_id)
        return "."


@dataclass
class Disk:
    blocks: list[Block] = field(default_factory=list)

    def walk(self):
        file_seeker = len(self.blocks) - 1
        while file_seeker > 0:
            block = self.blocks[file_seeker]
            if block.file_id is not None:
                self.find_empty_for_file_and_swap(block)
            file_seeker -= 1

    def find_empty_for_file_and_swap(self, block: Block):
        i = 0
        while i < block.run_start and i <= len(self.blocks):
            potential = self.blocks[i]
            if potential.file_id is None and potential.run_length >= block.run_length:
                self.swap_region(block, potential)
                return
            else:
                i = potential.run_end + 1

    def merge(self, run_a: Block, run_b: Block) -> None:
        if run_a.file_id == run_b.file_id:
            new_start = min(run_a.run_start, run_b.run_start)
            new_end = max(run_a.run_end, run_b.run_end)
            for i in range(new_start, new_end + 1):
                self.blocks[i].run_start = new_start
                self.blocks[i].run_end = new_end

    def merge_with_neighbors(self, idx: int) -> None:
        block = self.blocks[idx]
        if block.run_start > 0:
            left_neighbor = self.blocks[block.run_start - 1]
            self.merge(block, left_neighbor)
        if block.run_end + 1 < len(self.blocks):
            right_neighbor = self.blocks[block.run_end + 1]
            self.merge(block, right_neighbor)

    def swap_region(self, block_start: Block, space: Block) -> None:
        space_idx = space.run_start
        space_end = space.run_end
        new_start = space.run_start
        for block_idx in range(block_start.run_start, block_start.run_end + 1):
            block = self.blocks[block_idx]
            space = self.blocks[space_idx]
            self.swap(block_idx, space_idx)
            block.run_start = block.run_end = space_idx
            space.run_start = space.run_end = block_idx
            self.merge_with_neighbors(block_idx)
            self.merge_with_neighbors(space_idx)
            space_idx += 1
        for i in range(space_idx, space_end + 1):
            self.blocks[i].run_start = space_idx

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

    def append_file(self, file_id: int | None, length: int):
        start = len(self.blocks)
        end = start + length - 1
        for _ in range(length):
            self.blocks.append(Block(file_id, start, end))

    @classmethod
    def from_str(cls, rep: str) -> "Disk":
        disk = cls([])
        idx = 0
        for x, pair in enumerate(itertools.batched(rep, 2)):
            if len(pair) == 1:
                file_blocks_str = pair[0]
                empty_blocks_str = "0"
            else:
                file_blocks_str, empty_blocks_str = pair

            file_blocks = int(file_blocks_str)
            disk.append_file(x, file_blocks)
            empty_blocks = int(empty_blocks_str)
            disk.append_file(None, empty_blocks)
        return disk

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
