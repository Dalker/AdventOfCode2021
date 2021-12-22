"""
Advent of Code - tentative pour J22.

Daniel Kessler (aka Dalker), le 2021.12.22
"""

from __future__ import annotations  # waiting for python 3.10

import re

from copy import copy
from dataclasses import dataclass, replace
from itertools import product
from math import prod
from typing import Optional

import numpy as np


@dataclass
class Cuboid:
    min_coords: tuple[int, int, int]
    max_coords: tuple[int, int, int]

    @property
    def volume(self):
        """Volume of cuboid."""
        return prod(self.max_coords[j] - self.min_coords[j]
                    for j in range(3))

    def inter(self, other: Cuboid) -> Optional[Cuboid]:
        """Return intersection cuboid, if any."""
        min_coords = tuple(max(self.min_coords[j], other.min_coords[j])
                           for j in range(3))
        max_coords = tuple(min(self.max_coords[j], other.max_coords[j])
                           for j in range(3))
        if any(min_coords[j] > max_coords[j] for j in range(3)):
            return None
        return Cuboid(min_coords, max_coords)

    @staticmethod
    def bisect(original, axis: int, cutoff: int) -> tuple[Cuboid, Cuboid]:
        """Slice cuboid along given axis and return two sub-cuboids."""
        new_min_coords = list(original.min_coords)
        new_min_coords[axis] = cutoff
        new_max_coords = list(original.max_coords)
        new_max_coords[axis] = cutoff
        return (replace(original, max_coords=tuple(new_max_coords)),
                replace(original, min_coords=tuple(new_min_coords)))

    def minus(self, corner: Cuboid) -> list[Cuboid]:
        """
        Return cuboids adding up to self minus removed corner.

        Constraint: corner must be a cuboid within self, at one of its
        corners.
        """
        to_slice = self
        kept = []
        for dim in range(3):
            if self.min_coords[dim] == corner.min_coords[dim]:
                to_slice, to_keep = Cuboid.bisect(to_slice, dim,
                                                  corner.max_coords[dim])
            else:
                to_keep, to_slice = Cuboid.bisect(to_slice, dim,
                                                  corner.min_coords[dim])
            kept.append(to_keep)
        return kept


def get_data(fname: str) -> list[tuple[bool, Cuboid]]:
    """Read the day's input and return contents in adequate data structure."""
    lines = []
    with open(fname) as datafile:
        for line in datafile:
            on_off, cube = line.strip().split(' ')
            coords = re.search(r'x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)',
                               cube)
            lines.append((True if on_off == 'on' else False,
                          Cuboid(tuple(int(coords.group(n))
                                       for n in (1, 3, 5)),
                                 tuple(int(coords.group(n))
                                       for n in (2, 4, 6)))))
    return lines


def solve(data: list[tuple[bool, Cuboid]]) -> int:
    """Solve problem of the day."""
    cubes = np.zeros((101, 101, 101), dtype=bool)
    for on_off, cube in data:
        if any(coord > 50 for coord in cube.min_coords):
            continue
        if any(coord < -50 for coord in cube.max_coords):
            continue
        for x, y, z in product(*(range(cube.min_coords[i],
                                       cube.max_coords[i]+1)
                                 for i in range(3))):
            cubes[x+50, y+50, z+50] = on_off
    return cubes.sum()


def solve2(data: list[tuple[bool, Cuboid]]) -> int:
    """Solve part 2."""
    on_cubes = []
    for on_off, cube in data:
        new_on_cubes = copy(on_cubes)
        if on_off:  # got an "on" cuboid
            on_cubes.append(cube)
        else:  # got an "off" cuboid
            for on_cube in on_cubes:
                intersection = cube.inter(on_cube)
                if intersection is not None:
                    # subtract the part that was turned off
                    new_on_cubes.remove(on_cube)
                    new_on_cubes.extend(on_cube.minus(intersection))
                on_cubes = new_on_cubes
    return sum(cube.volume for cube in on_cubes)


if __name__ == "__main__":
    hintdata1 = get_data("hintdata22.txt")
    hintdata2 = get_data("hintdata22b.txt")
    realdata = get_data("input22.txt")
    print("check hint 1:", solve(hintdata1))
    print("  solution 1:", solve(realdata))
    print("check hint 2:", solve2(hintdata2))
    print("check hint 2:", 2758514936282235)
