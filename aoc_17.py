"""
Advent of Code - tentative pour J17.

Daniel Kessler (aka Dalker), le 2021.12.17
"""
from dataclasses import dataclass
from math import ceil

DAY = "17"


def get_data(fname: str) -> list[int]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        line = datafile.readline().strip()
    ind0, ind1 = line.find("="), line.find(",")
    xmin, xmax = line[ind0+1:ind1].split("..")
    ymin, ymax = line[line.find("=", ind1)+1:].split("..")
    return Area(*(int(n) for n in (xmin, xmax, ymin, ymax)))


@dataclass
class Area:
    """An area one can be inside of or not."""
    left: int
    right: int
    top: int
    bottom: int

    def __contains__(self, coords: tuple[int, int]) -> bool:
        x, y = coords
        return self.left <= x <= self.right and self.top <= y <= self.bottom


class Problem:
    """Problem of the day."""

    def __init__(self, area: Area):
        """Solve problem of the day."""
        self.area = area
        self.vx0min = ceil((-1 + (1 + 8*self.area.left)**.5/2))
        self.vy0min = self.area.top

    def solve(self) -> str:
        y_max = 0
        n_paths = 0
        for vx_init in range(self.vx0min, self.area.right + 1):
            for vy_init in range(self.area.top - 1, self.area.right + 1):
                vx, vy = vx_init, vy_init
                x, y = 0, 0
                current_ymax = 0
                while x <= self.area.right and y >= self.area.top:
                    x += vx
                    y += vy
                    vx = max(vx - 1, 0)
                    vy -= 1
                    current_ymax = max(current_ymax, y)
                    if (x, y) in self.area:
                        y_max = max(y_max, current_ymax)
                        n_paths += 1
                        break
        return f"y_max = {y_max:4d} , n_paths = {n_paths:4d}"


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("   check hint:", Problem(hintdata).solve())
    print("solve problem:", Problem(realdata).solve())
