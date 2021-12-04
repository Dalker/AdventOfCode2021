"""
Advent of Code - tentative pour J.

Daniel Kessler (aka Dalker), le 2021.12.
"""

DAY = "01"
HINTDATA = []


def get_data(fname: str) -> list[str]:
    """Read the day's input file and return contents as a list of ints."""
    try:
        with open(f"{fname}.txt") as datafile:
            data = [line for line in datafile]
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
        data = HINTDATA
    return data


def easy(data: str) -> str:
    """Easy problem of the day."""
    return ""


def hard(data: str) -> str:
    """Hard problem of the day."""
    return ""


if __name__ == "__main__":
    data = get_data(DAY)
    print("check hint 1:", easy(HINTDATA))
    print("check hint 2:", hard(HINTDATA))
    print("  solution 1:", easy(data))
    print("  solution 2:", hard(data))
