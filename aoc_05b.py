"""
Advent of Code - tentative pour J5.

Suite à la discussion sur Discord du jour, tentative de rendre
la résolution (beaucoup) plus efficace avec un Counter.

Daniel Kessler (aka Dalker), le 2021.12.
"""
from collections import Counter

DAY = "05"


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    try:
        with open(f"{fname}.txt") as datafile:
            data = list(datafile)
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
        return []
    return data


def sign(n: int) -> int:
    """Return signum of integer."""
    return 0 if n == 0 else (1 if n > 0 else -1)


def easy(data: list[str], diagonals=False) -> int:
    """Easy problem of the day."""
    counter = Counter()
    for line in data:
        x0, y0, x1, y1 = (int(n) for endpoint in line.split(" -> ")
                          for n in endpoint.split(","))
        dx, dy = sign(x1 - x0), sign(y1 - y0)
        if dx == 0:
            for y in range(y0, y1+dy, dy):
                counter[(x0, y)] += 1
        elif dy == 0:
            for x in range(x0, x1+dx, dx):
                counter[(x, y0)] += 1
        elif diagonals:
            for x, y in zip(range(x0, x1+dx, dx), range(y0, y1+dy, dy)):
                counter[(x, y)] += 1
    return sum(counter[key] > 1 for key in counter)


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
