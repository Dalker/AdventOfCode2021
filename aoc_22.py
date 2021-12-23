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

    def intersects(self, other: Cuboid) -> bool:
        """Determine if there is an intersection, without computing it."""
        if any(max(self.min_coords[dim], other.min_coords[dim])
               > min(self.max_coords[dim], other.max_coords[dim])
               for dim in range(3)):
            return False
        return True

    @staticmethod
    def bisect(original, axis: int, cutoff: int) -> tuple[Cuboid, Cuboid]:
        """Slice cuboid along given axis and return two sub-cuboids."""
        new_min_coords = tuple(cutoff if i == axis else original.min_coords[i]
                               for i in range(3))
        new_max_coords = tuple(cutoff if i == axis else original.max_coords[i]
                               for i in range(3))
        return (replace(original, max_coords=new_max_coords),
                replace(original, min_coords=new_min_coords))

    def minus(self, inner: Cuboid) -> list[Cuboid]:
        """Return cuboids adding up to self minus an inner cuboid."""
        to_slice = self
        parts = []
        for dim in range(3):
            left, to_slice = Cuboid.bisect(to_slice, dim,
                                           inner.min_coords[dim])
            to_slice, right = Cuboid.bisect(to_slice, dim,
                                            inner.max_coords[dim])
            parts.extend([left, right])
        return [part for part in parts if part.volume != 0]


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


def solve2a(data: list[tuple[bool, Cuboid]]) -> int:
    """Solve part 2."""
    on_cubes = []
    for on_off, cube in data:
        print("on" if on_off else "off", len(on_cubes))
        if on_off:  # got an "on" cuboid
            new_cubes = [cube]
            for on_cube in on_cubes:
                if not on_cube.inter(cube):
                    continue
                new_new_cubes = copy(new_cubes)
                for new_cube in new_cubes:
                    intersection = new_cube.inter(on_cube)
                    if intersection is not None:
                        new_new_cubes.remove(new_cube)
                        new_new_cubes.extend(new_cube.minus(on_cube))
                new_cubes = new_new_cubes
                print(len(new_cubes), "new cubes")
            on_cubes.extend(new_cubes)
        else:  # got an "off" cuboid
            new_on_cubes = copy(on_cubes)
            for on_cube in on_cubes:
                intersection = cube.inter(on_cube)
                if intersection is not None:
                    # subtract the part that was turned off
                    new_on_cubes.remove(on_cube)
                    new_on_cubes.extend(on_cube.minus(intersection))
            on_cubes = new_on_cubes
    return sum(cube.volume for cube in on_cubes)


def solve2b(data: list[tuple[bool, Cuboid]]) -> int:
    """Another take on part 2."""
    # first we discover all useful coordinates
    coords = [[], [], []]
    for _, cube in data:
        for dim in range(3):
            coords[dim].extend([cube.min_coords[dim], cube.max_coords[dim]])
    coords = [sorted(coord) for coord in coords]
    cuboids = []
    for enums in product(*(enumerate(coords[dim][:-1]) for dim in range(3))):
        low_bounds = tuple(enum[1] for enum in enums)
        hi_bounds = tuple(coords[dim][enum[0]+1]
                          for dim, enum in enumerate(enums))
        cuboids.append(Cuboid(low_bounds, hi_bounds))
    on_cuboids = []
    for on_off, cube in reversed(data):
        remaining_cuboids = copy(cuboids)
        print(len(cuboids), "remaining cuboids")
        for cuboid in cuboids:
            if cube.intersects(cuboid):
                remaining_cuboids.remove(cuboid)
                if on_off:
                    on_cuboids.add(cuboid)
        cuboids = remaining_cuboids
    volume = sum(cuboid.volume for cuboid in on_cuboids)
    return volume


def solve2c(data: list[tuple[bool, Cuboid]]) -> int:
    """Yet another take on part 2."""
    on_cuboids = []
    off_cuboids = []
    for on_off, cube in reversed(data):  # reversed time: fixed by last action
        print(len(on_cuboids), len(off_cuboids))
        print("on" if on_off else "off", cube)
        if on_off:  # cube is "on" except bits that are already fixed
            on_bits = [cube]
            for fixed_cube in off_cuboids + on_cuboids:
                if fixed_cube.intersects(cube):
                    new_on_bits = []
                    for bit in on_bits:
                        new_on_bits.extend(bit.minus(fixed_cube))
                    on_bits = new_on_bits
            on_cuboids.extend(on_bits)
        else:  # cube is "off": affects anything from the past
            off_cuboids.append(cube)
    return sum(cuboid.volume for cuboid in on_cuboids)


if __name__ == "__main__":
    hintdata1 = get_data("hintdata22.txt")
    hintdata2 = get_data("hintdata22b.txt")
    realdata = get_data("input22.txt")
    print("check hint 1:", solve(hintdata1))
    print("  solution 1:", solve(realdata))
    print("check hint 2:", solve2c(hintdata1))
    print("check hint 2:", 2758514936282235)
