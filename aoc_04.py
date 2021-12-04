"""
Advent of Code - tentative pour J4.

Daniel Kessler (aka Dalker), le 2021.12.04
"""
import _io  # for correct type annotation
from typing import Union
import numpy as np


class Bingo:
    """
    A bingo board.

    Attributes:
    - numbers: 5x5 numpy array of ints
    - beans: 5x5 numpy array of bool
    """

    def __init__(self, stream: Union[_io.TextIOWrapper, None] = None):
        if stream is None:
            self.numbers = []
            self.beans = []
            return
        numbers = []
        for _ in range(5):
            numbers.append([int(n) for n in stream.readline().split()])
        self.numbers = np.array(numbers)
        self.beans = np.zeros((5, 5), dtype=bool)

    def __str__(self):
        """Return nice representation for debugging purposes."""
        res = ""
        for row, numbers in enumerate(self.numbers):
            for col, number in enumerate(numbers):
                res += f"{number:3d}" + ("*" if self.beans[row, col] else " ")
            res += "\n"
        return res

    def __repr__(self):
        """Return ugly representation for debugging purposes."""
        return "Bingo(" + str(self.numbers) + ", " + str(self.beans) + ")"

    def copy(self):
        """Return a fresh copy of self."""
        clone = Bingo()
        clone.numbers = np.copy(self.numbers)
        clone.beans = np.copy(self.beans)
        return clone

    def place(self, called: int):
        """Check if a called number is in board and place bean if it is."""
        for row, numbers in enumerate(self.numbers):
            for col, number in enumerate(numbers):
                if number == called:
                    self.beans[row, col] = True

    def check(self):
        """Check if board won."""
        bingo = False
        for row in self.beans:
            if all(row):
                bingo = True
        for row in self.beans.transpose():
            if all(row):
                bingo = True
        # if bingo:
        #    print("bingo!")
        #    print(self)
        return bingo


def get_data(fname: str) -> (list[int], list[Bingo]):
    """Read the day's input file and return contents as a list of ints."""
    numbers = []
    boards = []
    try:
        with open(f"{fname}.txt") as datafile:
            numbers = [int(num) for num in datafile.readline().split(",")]
            while datafile.readline():
                boards.append(Bingo(datafile))
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
    return numbers, boards


def play_bingo(boards: list[Bingo], numbers: list[int],
               lose=False) -> (int, Bingo):
    """Play bingo with given boards and numbers until someone wins."""
    for number in numbers:
        for board in boards:
            already_won = board.check()
            board.place(number)
            if not already_won and board.check():
                last_winner = number, board.copy()
                if not lose:
                    return number, board
    return last_winner


def easy(data: (list[int], list[Bingo])) -> int:
    """Easy problem of the day."""
    numbers, boards = data
    winning_number, winner = play_bingo(boards, numbers)
    score = 0
    for row, numbers in enumerate(winner.numbers):
        for col, number in enumerate(numbers):
            if not winner.beans[row, col]:
                score += number
    return winning_number * score


def hard(data: str) -> str:
    """Hard problem of the day."""
    numbers, boards = data
    winning_number, winner = play_bingo(boards, numbers, lose=True)
    score = 0
    for row, numbers in enumerate(winner.numbers):
        for col, number in enumerate(numbers):
            if not winner.beans[row, col]:
                score += number
    return winning_number * score


if __name__ == "__main__":
    hintdata = get_data("hintdata04")
    data = get_data("input04")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(data))
    print("  solution 2:", hard(data))
