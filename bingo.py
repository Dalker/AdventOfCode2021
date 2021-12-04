"""
Advent of Code - tentative pour J4.

Classe Bingo utilisée effectivement lors de la résolution.
Cette classe a été extraite du fichier principal afin de pouvoir tester
une variante.

Daniel Kessler (aka Dalker), le 2021.12.04
"""
from typing import Union, TextIO
import numpy as np


class Bingo:
    """
    A bingo board.

    Attributes:
    - numbers: the playing card, a 5x5 numpy array of ints
    - beans: the beans placed on the card, a 5x5 numpy array of bool
    """

    def __init__(self, stream: Union[TextIO, None] = None):
        if stream is None:
            # good practice: always initialize all documented attributes
            # (and all public attributes should be documented in docstring)
            self.numbers = np.array([])
            self.beans = np.array([])
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
