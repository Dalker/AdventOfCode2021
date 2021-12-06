"""
Advent of Code - tentative pour J6.

Daniel Kessler (aka Dalker), le 2021.12.
"""
from copy import copy
from collections import Counter

DAY = "06"
HINTDATA = [3, 4, 3, 1, 2]


def get_data(fname: str) -> list[int]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = [int(n) for n in datafile.read().split(",")]
    return data


def easy(data: list[str], days: int = 80) -> int:
    """Easy problem of the day. Abandoned. Was inneficient at first."""
    for _ in range(days):
        born = len([True for n in data if n==0])
        future = [6 if n==0 else n-1 for n in data] + [8]*born
        data = future
        # print(data)
    return len(data)


def count(data: list[str], days) -> int:
    """Hard problem of the day. Have to be smarter."""
    fishcount = [0] * 9
    for n in data:
        fishcount[n] += 1
    for _ in range(days):
        newfishcount = [0] * 9
        for daycount in range(1, 9):
            newfishcount[daycount-1] = fishcount[daycount]
        newfishcount[8] = fishcount[0]
        newfishcount[6] += fishcount[0]
        fishcount = newfishcount
    return sum(fishcount)


if __name__ == "__main__":
    realdata = get_data(f"input{DAY}")
    print(easy(HINTDATA))
    print(easy(realdata))
    print("check hint 0:", count(HINTDATA, 18))
    print("check hint 1:", count(HINTDATA, 80))
    print("check hint 2:", count(HINTDATA, 256))
    print("  solution 0:", count(realdata, 18))
    print("  solution 1:", count(realdata, 80))
    print("  solution 2:", count(realdata, 256))
