"""
Advent of Code - tentative pour J25.

Daniel Kessler (aka Dalker), le 2021.12.25
"""

from __future__ import annotations  # waiting for python 3.10

from itertools import product

from copy import deepcopy

import numpy as np
import numpy.typing as npt


def get_data(fname: str) -> npt.NDArray:
    """Read the day's input and return contents in adequate data structure."""
    grid = []
    with open(fname) as datafile:
        for line in datafile:
            grid.append(list(line.strip()))
    return np.array(grid)


def step(grid: npt.NDArray) -> tuple[npt.NDArray, bool]:
    """Perform one step, return result and say if moved."""
    moved = False
    newgrid = deepcopy(grid)
    dim0, dim1 = grid.shape
    for coord0, coord1 in product(range(dim0), range(dim1)):
        if grid[coord0, coord1] == ">":
            new_coord1 = (coord1+1) % dim1
            if grid[coord0, new_coord1] == '.':
                newgrid[coord0, coord1] = '.'
                newgrid[coord0, new_coord1] = '>'
                moved = True
    grid = newgrid
    newgrid = deepcopy(grid)
    for coord0, coord1 in product(range(dim0), range(dim1)):
        if grid[coord0, coord1] == "v":
            new_coord0 = (coord0+1) % dim0
            if grid[new_coord0, coord1] == '.':
                newgrid[coord0, coord1] = '.'
                newgrid[new_coord0, coord1] = 'v'
                moved = True
    return newgrid, moved


def solve(grid: list[str]) -> int:
    """Solve problem of the day."""
    num = 0
    moved = True
    while moved:
        grid, moved = step(grid)
        num += 1
    return num


if __name__ == "__main__":
    hintdata = get_data("hintdata25.txt")
    realdata = get_data("input25.txt")
    print("check hint 1:", solve(hintdata))
    print("  solution 1:", solve(realdata))
