"""
Advent of Code - tentative pour J22.

Daniel Kessler (aka Dalker), le 2021.12.22
"""

from __future__ import annotations  # waiting for python 3.10

from dataclasses import dataclass
import re
from itertools import product, combinations, permutations
from collections import Counter, defaultdict, deque
from math import ceil, prod
from typing import Callable, Iterable, Optional, Union

import numpy as np


@dataclass
class Cube:
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int


def get_data(fname: str) -> list[tuple[bool, Cube]]:
    """Read the day's input and return contents in adequate data structure."""
    lines = []
    with open(fname) as datafile:
        for line in datafile:
            on_off, cube = line.strip().split(' ')
            coords = re.search(r'x=(.*)\.\.(.*),y=(.*)\.\.(.*),z=(.*)\.\.(.*)',
                               cube)
            lines.append((True if on_off == 'on' else False,
                          Cube(*(int(coords.group(i+1)) for i in range(6)))))
    return lines


def solve(data: list[str]) -> int:
    """Solve problem of the day."""
    cubes = np.zeros((101, 101, 101), dtype=bool)
    for on_off, cube in data:
        if cube.x_min > 50 or cube.y_min > 50 or cube.z_min > 50:
            continue
        if cube.x_max < -50 or cube.y_max < -50 or cube.z_max < -50:
            continue
        for x, y, z in product(range(cube.x_min, cube.x_max+1),
                               range(cube.y_min, cube.y_max+1),
                               range(cube.z_min, cube.z_max+1)):
            cubes[x+50, y+50, z+50] = on_off
    return cubes.sum()


if __name__ == "__main__":
    hintdata1 = get_data("hintdata22.txt")
    hintdata2 = get_data("hintdata22b.txt")
    realdata = get_data("input22.txt")
    print("check hint 1:", solve(hintdata1))
    print("  solution 1:", solve(realdata))
