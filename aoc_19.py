"""
Advent of Code - tentative pour J19.

Daniel Kessler (aka Dalker), le 2021.12.19
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product

import numpy as np
import numpy.typing as npt


class Scanner:
    """A Scanner with data from its beacons."""

    def __init__(self, identity: str):
        self.identity = identity
        self.beacons: list[tuple[int, ...]] = []
        self.matrix: npt.NDArray

    def __repr__(self) -> str:
        return (self.identity + "(" + ",".join(str(beacon) for beacon in
                                               self.beacons) + ")")

    def post_init(self):
        """Finish construction after all beacons are loaded."""
        self.n_beacons = len(self.beacons)
        self.matrix = np.zeros((self.n_beacons, 3))
        for n_beacon, beacon in enumerate(self.beacons):
            for dim in range(3):
                self.matrix[n_beacon][dim] = beacon[dim]

    def add_beacon(self, coords: tuple[int, ...]):
        """Add data about one beacon."""
        self.beacons.append(coords)

    def overlaps(self, other: Scanner):
        """Check for overlap of beacons."""
        self_col = self.matrix[:, 0]
        for dim, sign in product(range(3), (-1, +1)):
            other_col = sign * other.matrix[:, dim]
            diff_freq: dict[int, int] = Counter()
            for a, b in product(self_col, other_col):
                diff_freq[b - a] += 1
            for diff in diff_freq:
                if diff_freq[diff] >= 12:
                    return (dim, sign, diff, diff_freq[diff])
                    print(f"found >= 12 overlaps between {self.identity} "
                          f"and {other.identity} "
                          f"using params {dim}, {sign}, {diff}")
        return None


def get_data(fname: str) -> list[Scanner]:
    """Read the day's input and return contents in adequate data structure."""
    scanners: list[Scanner] = []
    scanner: Scanner
    with open(fname) as datafile:
        for line in datafile:
            if "scanner" in line:
                scanner = Scanner(line[4:-4])
                scanners.append(scanner)
            elif "," in line:
                scanner.add_beacon(tuple(int(val) for val in
                                         line.strip().split(",")))
    for scanner in scanners:
        scanner.post_init()
    return scanners


def solve(scanners: list[Scanner]) -> int:
    """Solve problem of the day."""
    n_scanners = len(scanners)
    for m, n in combinations(range(n_scanners), 2):
        overlaps = scanners[m].overlaps(scanners[n])
        if overlaps is not None:
            print("overlaps between scanners", m, n, overlaps)
    return n_beacons


if __name__ == "__main__":
    hintdata = get_data("hintdata19.txt")
    realdata = get_data("input19.txt")
    print("check hint 1:", solve(hintdata))
    print("  solution 1:", solve(realdata))  # 329 was too low!
    # print("check hint 2:", solve(hintdata, part2=True))
    # print("  solution 2:", solve(realdata, part2=True))
