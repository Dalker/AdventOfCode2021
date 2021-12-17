"""
Advent of Code - tentative pour J17.

Daniel Kessler (aka Dalker), le 2021.12.17
"""
from dataclasses import dataclass
from math import ceil


@dataclass
class Area:
    """An area one can be inside of or not."""
    left: int
    right: int
    top: int
    bottom: int

    def __contains__(self, coords: tuple[int, int]) -> bool:
        return (self.left <= coords[0] <= self.right and
                self.top <= coords[1] <= self.bottom)


def get_data(fname: str) -> Area:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        line = datafile.readline().strip()
    ind0, ind1 = line.find("="), line.find(",")
    xmin, xmax = line[ind0+1:ind1].split("..")
    ymin, ymax = line[line.find("=", ind1)+1:].split("..")
    return Area(*(int(n) for n in (xmin, xmax, ymin, ymax)))


def solve(area) -> str:
    """Solve both parts of day's problem."""
    # following was found with some pen and paper maths
    vx0min = ceil((-1 + (1 + 8*area.left)**.5/2))
    y_max = 0
    n_paths = 0
    for vx_init in range(vx0min, area.right + 1):
        # following has *not* been optimized but works for *actual data*
        for vy_init in range(area.top - 1, area.right + 1):
            # pylint: disable=C0103
            vx, vy = vx_init, vy_init
            x, y = 0, 0
            current_ymax = 0
            while x <= area.right and y >= area.top:
                x += vx
                y += vy
                vx = max(vx - 1, 0)
                vy -= 1
                current_ymax = max(current_ymax, y)
                if (x, y) in area:
                    y_max = max(y_max, current_ymax)
                    n_paths += 1
                    break
    return f"y_max = {y_max:4d} , n_paths = {n_paths:4d}"


if __name__ == "__main__":
    hintdata = get_data("hintdata17")
    realdata = get_data("input17")
    print("   check hint:", solve(hintdata))
    print("solve problem:", solve(realdata))
