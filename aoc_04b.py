"""
Advent of Code - tentative pour J4.

Version b avec dataclass BingoCard.

J'espérais ne rien devoir changer dans l'utilisation (donc l'interface) de
BingoCard, mais le constructeur (et copieur) nécessitent quelques modifs.
Du coup j'ai tout modifié et rendu plus compact ;-)

Daniel Kessler (aka Dalker), le 2021.12.04
"""
from itertools import product
from copy import deepcopy
from databingo import BingoCard

Data = tuple[list[int], list[BingoCard]]  # typing for today's data


def play_bingo(numbers: list[int], boards: list[BingoCard],
               lose=False) -> int:
    """Play bingo with given boards and numbers until someone wins."""
    for (number, board) in product(numbers, boards):
        already_won = board.check()
        board.call(number)
        if not lose and board.check():
            winning_board = board
            winning_number = number
            break
        if lose and not already_won and board.check():
            winning_board = deepcopy(board)
            winning_number = number
    score = sum(winning_board.numbers[coords]
                for coords in product(range(5), range(5))
                if not winning_board.beans[coords])
    return score * winning_number


def easy(data: Data) -> int:
    """Easy problem of the day."""
    return play_bingo(*data)


def hard(data: Data) -> int:
    """Hard problem of the day. Actually easier than easy this time!"""
    return play_bingo(*data, lose=True)


def get_data(fname: str) -> Data:
    """Read the day's input file and return contents as a list of ints."""
    with open(f"{fname}.txt") as datafile:
        numbers = [int(num) for num in datafile.readline().split(",")]
        boards = []
        while datafile.readline():  # blank line available => card available
            boards.append(BingoCard().read(datafile))
    return numbers, boards


if __name__ == "__main__":
    hintdata = get_data("hintdata04")
    data = get_data("input04")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(data))
    print("  solution 2:", hard(data))
