"""
Advent of Code - tentative pour J<n>.

Daniel Kessler (aka Dalker), le 2021.12.
"""
from itertools import product
import numpy as np

DAY = "05"


class Segment:
    """A segment with all its intermediate integer-located points."""

    def __init__(self, *coords):
        self.x0, self.y0, self.x1, self.y1 = coords
        # print(coords, "is not" if not self.is_diagonal() else "is", "diagonal")

    def __str__(self) -> str:
        return f"segment from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1})."

    def is_diagonal(self) -> bool:
        return self.x0 != self.x1 and self.y0 != self.y1

    def __iter__(self):
        if self.x0 == self.x1:
            ymin, ymax = sorted([self.y0, self.y1])
            return product([self.x0], range(ymin, ymax+1))
        elif self.y0 == self.y1:
            xmin, xmax = sorted([self.x0, self.x1])
            return product(range(xmin, xmax+1), [self.y0])
        else:
            dx = 1 if self.x0 < self.x1 else -1
            dy = 1 if self.y0 < self.y1 else -1
            return zip(range(self.x0, self.x1 + dx, dx),
                       range(self.y0, self.y1 + dy, dy))
        return self


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    try:
        with open(f"{fname}.txt") as datafile:
            data = list(datafile)
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
        return []
    return data


def easy(data: list[str], diagonals=False) -> int:
    """Easy problem of the day."""
    DEBUG = False
    segments = []
    xmax, ymax = 0, 0
    for line in data:
        x0, y0, x1, y1 = (int(n) for endpoint in line.split(" -> ")
                          for n in endpoint.split(","))
        xmax, ymax = max(xmax, x0, x1), max(ymax, y0, y1)
        segments.append(Segment(x0, y0, x1, y1))
    grid = np.zeros((xmax+1, ymax+1))
    for segment in segments:
        if not diagonals and segment.is_diagonal():
            continue
        if DEBUG:
            print("processing", segment)
        for x, y in segment:
            if DEBUG:
                print(x, y, end=", ")
            grid[x, y] += 1
        if DEBUG:
            print()
    if DEBUG:
        print(grid.transpose())
    return sum(value > 1 for row in grid for value in row)


def hard(data: list[str]) -> int:
    """Hard problem of the day."""
    return easy(data, diagonals=True)


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(realdata))
    print("  solution 2:", hard(realdata))
