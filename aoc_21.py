"""
Advent of Code - tentative pour J21.

Daniel Kessler (aka Dalker), le 2021.12.21
"""

from __future__ import annotations  # waiting for python 3.10

from ast import literal_eval
from itertools import product, combinations, permutations
from collections import Counter, defaultdict, deque
from math import ceil, prod
from typing import Callable, Iterable, Optional, Union


def get_data(fname: str) -> list[int]:
    """Read the day's input and return contents in adequate data structure."""
    with open(fname) as datafile:
        data = [int(line.strip().split(":")[1]) for line in datafile]
    return data


def warmup(positions: list[int]) -> int:
    """Solve problem of the day."""
    rolls = dieface = turn = 0
    positions = [position - 1 for position in positions]
    scores = [0, 0]
    while all(score < 1000 for score in scores):
        move = 0
        for _ in range(3):
            dieface += 1
            if dieface == 101:
                dieface = 1
            move += dieface
        positions[turn] = (positions[turn] + move) % 10
        scores[turn] += positions[turn] + 1
        turn = (turn+1) % 2
        rolls += 3
    print(scores, rolls)
    return min(scores) * rolls


# number of ways to get each result in 3 rolls (= nb universes)
RESULT_COUNT = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


def dirac(positions: list[int]) -> int:
    """Solve the real problem of the day."""
    universes = {(0, 0, 0, 0): 1}  # pos0-1, pos1-1, score0, score1: count
    turn = 0
    while any(score[2] < 21 and score[3] < 21 for score in universes):
        new_universes = Counter()
        for universe, count1 in universes.items():
            pos0, pos1, score0, score1 = universe
            for result, count2 in RESULT_COUNT.items():
                if score0 >= 21 or score1 >= 21:
                    new_universes[universe] = score1
                elif turn == 0:
                    new_pos0 = (pos0 + result) % 10
                    new_score0 = score0 + new_pos0 + 1
                    new_universes[(new_pos0, pos1,
                                   new_score0, score1)] += count1*count2
                else:
                    new_pos1 = (pos1 + result) % 10
                    new_score1 = score1 + new_pos1 + 1
                    new_universes[(pos0, new_pos1,
                                   score0, new_score1)] += count1*count2
        universes = new_universes
        turn = (turn+1) % 2
    wins0 = sum(count for score, count in universes.items() if score[2] >
                score[3])
    wins1 = sum(count for score, count in universes.items() if score[2] <
                score[3])
    return wins0, wins1


if __name__ == "__main__":
    hintdata = get_data("hintdata21.txt")
    realdata = get_data("input21.txt")
    print("check hint 1:", warmup(hintdata))
    print("  solution 1:", warmup(realdata))
    print("check hint 2:", dirac(hintdata))
