"""
Advent of Code - tentative pour J4.

Variante de la classe Bingo, pour s'amuser avec les Data Classes.

Les fonctions magiques __init__ et __str__ sont créées de manière
automatique, et les copies fonctionne bien (pour tester __str__,
il suffit d'ajouter un print(board) quelque part dans le programme
principal pour voir le résultat).

Daniel Kessler (aka Dalker), le 2021.12.04
"""
from itertools import product
from dataclasses import dataclass, field
from typing import TextIO
import numpy as np
import numpy.typing as npt


@dataclass
class BingoCard:
    """
    A bingo card, possibly with some beans on it.

    Attributes:
    - numbers: the playing card, a 5x5 numpy array of ints
    - beans: the beans placed on the card, a 5x5 numpy array of bool
    """
    # NB: le typage des classes de numpy n'est pas documenté de manière très
    # claire... mais ce qui suit fonctionne et est accepté par mypy
    numbers: npt.NDArray[np.int_] = field(default_factory=lambda: np.array([]))
    beans: npt.NDArray[np.bool_] = field(default_factory=lambda:
                                         np.zeros((5, 5), dtype=bool))

    def read(self, stream: TextIO):
        """Read 5 lines of data from input stream into the bingo card."""
        self.numbers = np.array([[int(n) for n in stream.readline().split()]
                                for _ in range(5)])
        return self  # to allow chaining with default constructor

    def call(self, called: int):
        """Place bean in called number's location if number is on card."""
        for location in (coords for coords in product(range(5), range(5))
                         if self.numbers[coords] == called):
            self.beans[location] = True

    def check(self):
        """Check if board won."""
        return (any(all(row) for row in self.beans)
                or any(all(row) for row in self.beans.transpose()))
