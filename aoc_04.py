"""
Advent of Code - tentative pour J4.

Daniel Kessler (aka Dalker), le 2021.12.04
"""
from bingo import Bingo

Data = tuple[list[int], list[Bingo]]  # typing for today's data


def play_bingo(boards: list[Bingo], numbers: list[int],
               lose=False) -> tuple[int, Bingo]:
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


def easy(data: Data) -> int:
    """Easy problem of the day."""
    numbers, boards = data
    winning_number, winner = play_bingo(boards, numbers)
    score = 0
    for row, numbers in enumerate(winner.numbers):
        for col, number in enumerate(numbers):
            if not winner.beans[row, col]:
                score += number
    return winning_number * score


def hard(data: Data) -> int:
    """Hard problem of the day. Actually easier than easy this time!"""
    numbers, boards = data
    winning_number, winner = play_bingo(boards, numbers, lose=True)
    score = 0
    for row, numbers in enumerate(winner.numbers):
        for col, number in enumerate(numbers):
            if not winner.beans[row, col]:
                score += number
    return winning_number * score


def get_data(fname: str) -> Data:
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


if __name__ == "__main__":
    hintdata = get_data("hintdata04")
    data = get_data("input04")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(data))
    print("  solution 2:", hard(data))
