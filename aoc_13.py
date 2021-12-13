"""
Advent of Code - tentative pour J13.

Daniel Kessler (aka Dalker), le 2021.12.13
"""

import numpy as np

DAY = "13"


def get_data(fname: str) -> tuple[set[tuple[int, int]],
                                  list[tuple[str, int]]]:
    """Read the day's input and return contents in adequate data structure."""
    coords = set()
    instructions = []
    with open(f"{fname}.txt") as datafile:
        for line in datafile:
            if line == "\n":
                break
            coords.add(tuple(int(n)
                             for n in line.strip().split(",")))
        for line in datafile:
            instr = line.split()[-1].split("=")
            instructions.append((instr[0], int(instr[1])))
    return coords, instructions


def fold_x(coords: set[tuple[int, int]], sym: int) -> set[tuple[int, int]]:
    """Fold paper along a horizontal axis."""
    res = set()
    for x, y in coords:
        if x < sym:
            res.add((x, y))
        else:
            res.add((2*sym - x, y))
    return res


def fold_y(coords: set[tuple[int, int]], sym: int) -> set[tuple[int, int]]:
    """Fold paper along a horizontal axis."""
    res = set()
    for x, y in coords:
        if y < sym:
            res.add((x, y))
        else:
            res.add((x, 2*sym - y))
    return res


def read(coords: set[tuple[int, int]]):
    """Read the code."""
    x_max = max(x for x, y in coords)
    y_max = max(y for x, y in coords)
    print(x_max, y_max)
    grid = [[" "] * (x_max+1) for _ in range(y_max+1)]
    for x, y in coords:
        grid[y][x] = "*"
    for line in grid:
        print("".join(line))
        


def solve(coords: set[tuple[int, int]],
          instructions: list[tuple[str, int]],
          part2: bool = False) -> int:
    """Solve problem of the day."""
    for axis, number in instructions:
        if axis == "x":
            coords = fold_x(coords, number)
        else:
            coords = fold_y(coords, number)
        if not part2:
            break
    if part2:
        read(coords)
    return len(coords)


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(*hintdata))
    print("check hint 2:", solve(*hintdata, part2=True))
    print("  solution 1:", solve(*realdata))
    print("  solution 2:", solve(*realdata, part2=True))
