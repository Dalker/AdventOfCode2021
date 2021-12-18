"""
Advent of Code - tentative pour J18.

Daniel Kessler (aka Dalker), le 2021.12.18
"""

from __future__ import annotations  # needed until python 3.10

from typing import Optional, Iterable
from collections import deque
from itertools import permutations


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    with open(fname) as datafile:
        data = [line.strip() for line in datafile]
    return data


class SFN:
    """SnailFish Number Binary Tree.

    A node of a binary tree that either contains an int value or has
    both a left and a right child.
    """

    def __init__(self, parent: Optional[SFN] = None,
                 value: Optional[int] = None):
        self.parent: Optional[SFN] = parent
        self.left_child: Optional[SFN] = None
        self.right_child: Optional[SFN] = None
        self.left_neighbour: Optional[SFN] = None
        self.right_neighbour: Optional[SFN] = None
        self.value: Optional[int] = value

    def __repr__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return ("[" + repr(self.left_child) + ","
                    + repr(self.right_child) + "]")

    def __add__(self, other: SFN):
        result = self.parse(f"[{self},{other}]")
        while True:
            # print(result)
            if result.explode():
                continue
            if result.split():
                continue
            break
        return result

    @property
    def magnitude(self):
        """Return magnitude of the SnailFish Number."""
        if self.value is not None:
            return self.value
        return 3*self.left_child.magnitude + 2*self.right_child.magnitude

    @staticmethod
    def sum(terms: Iterable[str]):
        """Add all SFNs on the iterable."""
        termsq = deque(terms)
        result = SFN.parse(termsq.popleft())
        while termsq:
            result = result + SFN.parse(termsq.popleft())
        return result

    def create_pair(self):
        """Create a pair of empty children on tree."""
        self.left_child, self.right_child = SFN(self), SFN(self)

    def split(self) -> bool:
        """Split a number into two parts."""
        current = self
        while current.left_child is not None:
            current = current.left_child
        while current is not None and current.value < 10:  # type: ignore
            current = current.right_neighbour
        if current is not None:
            assert current.value is not None
            current.left_child = SFN(current, current.value // 2)
            current.right_child = SFN(current, current.value // 2
                                      + current.value % 2)
            if current.left_neighbour is not None:
                current.left_child.left_neighbour = current.left_neighbour
                current.left_neighbour.right_neighbour = current.left_child
            if current.right_neighbour is not None:
                current.right_child.right_neighbour = current.right_neighbour
                current.right_neighbour.left_neighbour = current.right_child
            current.left_child.right_neighbour = current.right_child
            current.right_child.left_neighbour = current.left_child
            current.value = None
            return True
        return False

    def explode(self, level=0) -> bool:
        """Explode a pair, sending parts to the left and right."""
        if level == 4 and self.value is None:
            self.value = 0
            left = self.left_child.left_neighbour
            right = self.right_child.right_neighbour
            if left is not None:
                left.value += self.left_child.value
                self.left_neighbour = left
                left.right_neighbour = self
            if right is not None:
                right.value += self.right_child.value
                self.right_neighbour = right
                right.left_neighbour = self
            self.left_child = self.right_child = None
            return True
        if level == 4 or self.value is not None:
            return False
        return (self.left_child.explode(level+1) or
                self.right_child.explode(level+1))

    @staticmethod
    def parse(sfnumber: str):
        """Parse a snailfish number and return parse tree root."""
        root = SFN()
        current = root
        lastvalued = None
        for symbol in sfnumber:
            if symbol == "[":
                current.create_pair()
                current = current.left_child
            elif symbol == ",":
                current = current.parent.right_child
            elif symbol == "]":
                current = current.parent
            else:
                current.value = int(symbol)
                if lastvalued is not None:
                    lastvalued.right_neighbour = current
                    current.left_neighbour = lastvalued
                lastvalued = current
        assert repr(root) == sfnumber
        return root


def test_explosion():
    """Assert that all explosion tests work."""
    tests = {"[[[[[9,8],1],2],3],4]": "[[[[0,9],2],3],4]",
             "[7,[6,[5,[4,[3,2]]]]]": "[7,[6,[5,[7,0]]]]",
             "[[6,[5,[4,[3,2]]]],1]": "[[6,[5,[7,0]]],3]",
             "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]":
             "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
             "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]":
             "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"}
    for before, after in tests.items():
        sfn = SFN.parse(before)
        sfn.explode()
        assert repr(sfn) == after, f"explode({before}) != {after}"


def test_sums():
    """Perform all test sums."""
    print(SFN.sum(["[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]"]))
    print(SFN.sum(["[1,1]", "[2,2]", "[3,3]", "[4,4]"]))
    print(SFN.sum(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]))
    print(SFN.sum(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"]))
    hintdatas = get_data("hintdata18a.txt")
    print(SFN.sum(hintdatas))


def test_magnitudes():
    """Assert that all test magnitudes work."""
    assert SFN.parse("[9,1]").magnitude == 29
    assert SFN.parse("[[1,2],[[3,4],5]]").magnitude == 143
    assert SFN.parse("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude == 3488


def max_magnitude(assignments: list[str]):
    """Find the maximal magnitude of pairwise sums."""
    sfns = [SFN.parse(assignment) for assignment in assignments]
    return max((sfn1 + sfn2).magnitude for sfn1, sfn2 in permutations(sfns, 2))


if __name__ == "__main__":
    test_explosion()
    # test_sums()
    test_magnitudes()
    hintdata = get_data("hintdata18.txt")
    hintpart1 = SFN.sum(hintdata)
    print(hintpart1, hintpart1.magnitude)
    print(max_magnitude(hintdata))
    realdata = get_data("input18.txt")
    realpart1 = SFN.sum(realdata)
    print(realpart1, realpart1.magnitude)
    print(max_magnitude(realdata))
