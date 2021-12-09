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
    unprocessed = [point]
    basin = []
    while unprocessed:
        x, y = unprocessed.pop()
        basin.append((x, y))
        value = grid[x, y]
        for (dx, dy) in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            other = grid[x+dx, y+dy]
            if value < other < 9:
                unprocessed.append((x+dx, y+dy))
    return len(set(basin))


def pad(rawdata: list[list[int]]) -> tuple[npt.NDArray, int, int]:
    """Turn into array and pad with tens."""
    arr = np.array(rawdata)
    (m, n) = np.shape(arr)
    v_pad = 10 * np.ones((m, 1),  int)
    h_pad = 10 * np.ones((1, n+2), int)
    arr = np.concatenate((h_pad,
                          np.concatenate((v_pad, arr, v_pad),  axis=1),
                          h_pad), axis=0)
    return arr, m, n


def solve(data: list[list[int]]) -> tuple[int, int]:
    """Solve problem of the day."""
    risk = 0
    points, dim0, dim1 = pad(data)
    basin_sizes = []
    for (i, j) in product(range(dim0), range(dim1)):
        i, j = i+1, j+1
        if points[i, j] < min(points[i+1, j], points[i-1, j], points[i, j-1],
                              points[i, j+1]):
            risk += points[i, j] + 1
            basin_sizes.append(basin_size(points, (i, j)))
    basin_sizes = sorted(basin_sizes, reverse=True)
    return risk, math.prod(basin_sizes[:3])


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint:", solve(hintdata))
    print("  solution:", solve(realdata))
