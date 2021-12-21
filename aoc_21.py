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
    # count of nb of universes with each score
    scores = {(0, 0): 1}
    turn = 0
    while any(score[0] < 21 and score[1] < 21 for score in scores):
        new_scores = Counter()
        for score, count1 in scores.items():
            for result, count2 in RESULT_COUNT.items():
                new_score0 = score[0] + result if turn == 0 else score[0]
                new_score1 = score[1] + result if turn == 1 else score[1]
                new_scores[(new_score0, new_score1)] += count1*count2
        scores = new_scores
        turn = (turn+1) % 2
    wins0 = sum(count for score, count in scores.items() if score[0] > score[1])
    wins1 = sum(count for score, count in scores.items() if score[0] < score[1])
    return wins0, wins1


if __name__ == "__main__":
    hintdata = get_data("hintdata21.txt")
    realdata = get_data("input21.txt")
    print("check hint 1:", warmup(hintdata))
    print("  solution 1:", warmup(realdata))
    print("check hint 2:", dirac(hintdata))
