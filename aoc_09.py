"""
Advent of Code - tentative pour J<n>.

Daniel Kessler (aka Dalker), le 2021.12.<n>
"""
import math
from itertools import product

import numpy as np
import numpy.typing as npt

DAY = "09"


def get_data(fname: str) -> list[list[int]]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = [[int(number) for number in line.strip()]
                for line in datafile]
    return data


def basin_size(grid: npt.NDArray, point: tuple[int, int]) -> int:
    """Get size of basin around (m, n)."""
    # use sets to avoid duplicates in case of multiple paths to same point
    unprocessed = {point}
    basin = set()
    while unprocessed:
        x, y = unprocessed.pop()
        basin.add((x, y))
        value = grid[x, y]
        for (dx, dy) in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            other = grid[x+dx, y+dy]
            if value < other < 9:
                unprocessed.add((x+dx, y+dy))
    return len(basin)


def solve(data: list[list[int]]) -> tuple[int, int]:
    """Solve problem of the day."""
    risk = 0
    points = np.pad(data, 1, constant_values=10)
    basin_sizes = []
    for (i, j) in product(*(range(1, points.shape[dim]-1) for dim in (0, 1))):
        if points[i, j] < min(points[i-1, j], points[i+1, j],
                              points[i, j-1], points[i, j+1]):
            risk += points[i, j] + 1
            basin_sizes.append(basin_size(points, (i, j)))
    basin_sizes = sorted(basin_sizes, reverse=True)
    return risk, math.prod(basin_sizes[:3])


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint:", solve(hintdata))
    print("  solution:", solve(realdata))
