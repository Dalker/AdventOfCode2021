"""
Advent of Code - tentative pour J11.

Daniel Kessler (aka Dalker), le 2021.12.11
"""
from itertools import product
from copy import deepcopy

import numpy as np
import numpy.typing as npt

DAY = "11"


def get_data(fname: str) -> npt.NDArray[int]:
    """Read the day's input and return contents in adequate data structure."""
    data = []
    with open(f"{fname}.txt") as datafile:
        for line in datafile:
            data.append([int(n) for n in list(line.strip())])
    return np.array(data)


def step(energies: npt.NDArray[int]) -> npt.NDArray[int]:
    """Perform one step of dumbo octopus evolution."""
    m, n = energies.shape
    # first,  increase each octopus' energy by 1
    for i, j in product(range(m), range(n)):
        energies[i, j] += 1
    # the flash as much as possible
    while any(energy > 9 for energy in energies.flatten()):
        for x, y in product(range(m), range(n)):
            if energies[x, y] > 9:
                energies[x, y] = 0
                for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
                    # mon try...except causait plus de bugs qu'autre chose
                    # donc je change pour une vérification d'intervalle
                    if 0 <= x+dx < m and 0 <= y+dy < n:
                        if energies[x+dx, y+dy] != 0:
                            energies[x+dx, y+dy] += 1


def solve(octopi: npt.NDArray[int]) -> int:
    """Solve problem of the day."""
    flashes = 0
    for n in range(100):
        # print(f"step {n}")
        # print(octopi)
        step(octopi)
        flashes += sum([octopus == 0 for octopus in octopi.flatten()])
    return flashes


def solve2(octopi: npt.NDArray[int]) -> int:
    """Solve second part."""
    dim_x, dim_y = octopi.shape
    for n in range(1000):
        step(octopi)
        if all(octopi[i, j] == octopi[0, 0]
               for (i, j) in product(range(dim_x), range(dim_y))):
            return n+1
    return -1


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(deepcopy(hintdata)))
    print("check hint 2:", solve2(hintdata))
    print("  solution 1:", solve(deepcopy(realdata)))
    print("  solution 2:", solve2(realdata))
