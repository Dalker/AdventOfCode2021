"""
Advent of Code - tentative pour J19.

Daniel Kessler (aka Dalker), le 2021.12.19
"""
from __future__ import annotations

from copy import copy
from collections import Counter
from itertools import permutations, product

import numpy as np
import numpy.typing as npt


class Scanner:
    """A Scanner with data from its beacons."""

    def __init__(self, identity: str):
        self.identity = identity
        self.beacons: list[tuple[int, ...]] = []
        self.n_beacons = 0
        self.matrix: npt.NDArray
        self.location = np.zeros(3, dtype=int)

    def __repr__(self) -> str:
        return (self.identity + "(" + ",".join(str(beacon) for beacon in
                                               self.beacons) + ")")

    def post_init(self):
        """Finish construction after all beacons are loaded."""
        self.n_beacons = len(self.beacons)
        self.matrix = np.zeros((self.n_beacons, 3), dtype=int)
        for n_beacon, beacon in enumerate(self.beacons):
            for dim in range(3):
                self.matrix[n_beacon][dim] = beacon[dim]

    def add_beacon(self, coords: tuple[int, ...]):
        """Add data about one beacon."""
        self.beacons.append(coords)

    def overlaps(self, other: Scanner) -> bool:
        """Check for overlap of beacons, adjusting other if possible."""
        for dims, signs in product(permutations(range(3)),
                                   product((-1, +1), repeat=3)):
            diff_freq: dict[tuple[int, ...], int] = Counter()
            # pylint: disable=C0103
            for m, n in product(range(self.n_beacons), range(other.n_beacons)):
                diff_freq[tuple(self.matrix[m, i]
                                - signs[i] * other.matrix[n, dims[i]]
                                for i in range(3))] += 1
            for diff, freq in diff_freq.items():
                if freq >= 12:
                    # print(dims, signs, diff)
                    new_matrix = np.column_stack([signs[i]
                                                  * other.matrix[:, dims[i]]
                                                  + diff[i]
                                                  for i in range(3)])
                    other.matrix = new_matrix
                    other.location += np.array(diff)
                    return True
        return False


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


def longest_distance(scanners: list[Scanner]) -> int:
    """Find longest Manhattan distance between two scanners."""
    def manhattan(a: npt.NDArray, b: npt.NDArray):  # pylint: disable=C0103
        return sum(abs(a[i] - b[i]) for i in range(len(a)))
    return max(manhattan(s1.location, s2.location)
               for s1, s2 in permutations(scanners, 2))


def solve(scanners: list[Scanner]) -> tuple[int, int]:
    """Solve problem of the day."""
    not_adjusted = list(range(1, len(scanners)))
    queue = [0]
    current = 0
    while queue:
        for other in copy(not_adjusted):
            if scanners[current].overlaps(scanners[other]):
                print("overlaps between scanners", current, "and", other)
                # scanners[current].adjust(scanners[other], *overlaps)
                not_adjusted.remove(other)
                queue.append(other)
        current = queue.pop()
    assert not_adjusted == []
    beacons = []
    for scanner in scanners:
        for n_beacon in range(scanner.n_beacons):
            beacon = list(scanner.matrix[n_beacon, :])
            if beacon not in beacons:
                beacons.append(beacon)
    return len(beacons), longest_distance(scanners)


if __name__ == "__main__":
    hintdata = get_data("hintdata19.txt")
    realdata = get_data("input19.txt")
    print("check hint 1:", solve(hintdata))
    print("  solution 1:", solve(realdata))  # 329 was too low!
