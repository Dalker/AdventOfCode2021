"""
Advent of Code - tentative pour J18.

Daniel Kessler (aka Dalker), le 2021.12.18
"""

from __future__ import annotations  # needed until python 3.10

from typing import Optional, Union


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    with open(fname) as datafile:
        data = list(datafile)
    return data


class SNF:
    """SnailFish Number Binary Tree."""

    def __init__(self, parent: Optional[SNF] = None,
                 value: Optional[int] = None):
        self.parent: Optional[SNF] = parent
        self.value: Union[int, tuple[SNF, SNF], None] = value

    def __repr__(self):
        return ("[" + repr(self.left) + "," + repr(self.right) + "]"
                if isinstance(self.value, tuple)
                else repr(self.value))

    @property
    def left(self) -> SNF:
        return self.value[0]

    @property
    def right(self) -> SNF:
        return self.value[1]

    def first_left(self) -> Optional[int]:
        if isinstance(self.left, int):
            return self.left
        elif isinstance(self.left, SNF):
            return self.left.first_left()
        else:
            return self.parent.first_left()

    def create_pair(self):
        self.value = SNF(self), SNF(self)

    def explode(self, level=0):
        if level == 4:
            if isinstance(self.value, int):
                return False
            return True
        if isinstance(self.value, int):
            return False
        if self.left.explode(level+1):
            return True
        if self.right.explode(level+1):
            return True
        return False

    @staticmethod
    def parse(sfnumber: str):
        """Parse a snailfish number and return parse tree root."""
        root = SNF()
        current = root
        for symbol in sfnumber:
            if symbol == "[":
                current.create_pair()
                current = current.left
            elif symbol == ",":
                current = current.parent.right
            elif symbol == "]":
                current = current.parent
            else:
                current.value = int(symbol)
        assert repr(root) == sfnumber
        print(repr(root) + (" can explode" if root.explode() else " can't explode"))
        return root


def solve(data: list[str], part2: bool = False) -> int:
    """Solve problem of the day."""
    return 0


if __name__ == "__main__":
    SNF.parse("[[[[[9,8],1],2],3],4]")
    SNF.parse("[[[[0,1],2],3],4]")
    hintdata = get_data("hintdata18.txt")
    realdata = get_data("input18.txt")
    print("check hint 1:", solve(hintdata))
    # print("  solution 1:", solve(realdata))
    # print("check hint 2:", solve(hintdata, part2=True))
    # print("  solution 2:", solve(realdata, part2=True))
