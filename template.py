"""
Advent of Code - tentative pour J<n>.

Daniel Kessler (aka Dalker), le 2021.12.<n>
"""

from __future__ import annotations  # waiting for python 3.10

from ast import literal_eval
from itertools import product, combinations, permutations
from collections import Counter, defaultdict, deque
from math import ceil, prod
from typing import Callable, Iterable, Optional, Union


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    with open(fname) as datafile:
        data = list(line.strip() for line in datafile)
    return data


def solve(data: list[str]) -> int:
    """Solve problem of the day."""
    return 0


if __name__ == "__main__":
    hintdata = get_data("hintdata<n>.txt")
    realdata = get_data("input<n>.txt")
    print("check hint 1:", solve(hintdata))
    # print("  solution 1:", solve(realdata))
