"""
Advent of Code - tentative pour J22.

Daniel Kessler (aka Dalker), le 2021.12.22
"""

from __future__ import annotations  # waiting for python 3.10

import re
from dataclasses import dataclass
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

    def minus_inter(self, inter: Cuboid) -> list[Cuboid]:
        """
        Give cuboids corresponding to self minus inter.

        Constraint: inter must be a cuboid within self, at one of its
        corners.
        """
        floor_min_z = inter.min_coords[2]
        front_min_y = inter.min_coords[1]
        if self.min_coords[2] == inter.min_coords[2]:
            floor_max_z = inter.max_coords[2]
            rest_z = Cuboid((self.min_coords[0],
                             self.min_coords[1],
                             floor_max_z), self.max_coords)
        else:
            floor_max_z = self.max_coords[2]
            rest_z = Cuboid((self.min_coords,
                             (self.max_coords[0],
                              self.max_coords[1],
                              floor_min_z)))
        if self.min_coords[1] == inter.min_coords[1]:
            front_max_y = inter.max_coords[1]
            rest_y = Cuboid((self.min_coords[0],
                             front_max_y, floor_min_z),
                            (self.max_coords[0], self.max_coords[1],
                             floor_max_z))
        else:
            front_max_y = self.max_coords[1]
            rest_y = Cuboid((self.min_coords[0], self.min_coords[1],
                             floor_min_z),
                            (self.min_coords[0],
                             front_min_y, floor_max_z))
        if self.min_coords[0] == inter.min_coords[0]:
            rest_x = Cuboid((inter.max_coords[0], front_min_y, floor_min_z),
                            (self.max_coords[0], front_max_y, floor_max_z))
        else:
            rest_x = Cuboid((self.min_coords[0], front_min_y, floor_min_z),
                            (inter.min_coords[0], front_max_y, floor_max_z))
        return [rest_x, rest_y, rest_z]


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
    off_cubes = []  # cubes that must be subtracted from ons
    for on_off, cube in data:
        if on_off:  # got an "on" cuboid
            on_cubes.append(cube)
            for off_cube in off_cubes:
                intersection = cube.inter(off_cube)
                if intersection is not None:
                    # compensate an existing subtraction
                    on_cubes.append(intersection)
        else:  # got an "off" cuboid
            for on_cube in on_cubes:
                intersection = cube.inter(on_cube)
                if intersection is not None:
                    # subtract the part that was turned off
                    off_cubes.append(intersection)
    print(len(on_cubes), len(off_cubes))
    return (sum(cube.volume for cube in on_cubes)
            - sum(cube.volume for cube in off_cubes))


if __name__ == "__main__":
    hintdata1 = get_data("hintdata22.txt")
    hintdata2 = get_data("hintdata22b.txt")
    realdata = get_data("input22.txt")
    print("check hint 1:", solve(hintdata1))
    print("  solution 1:", solve(realdata))
    print("check hint 2:", solve2(hintdata2))
    print("check hint 2:", 2758514936282235)
