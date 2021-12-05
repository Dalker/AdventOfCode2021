"""
Advent of Code - tentative pour J<n>.

Daniel Kessler (aka Dalker), le 2021.12.
"""

DAY = "0<n>"


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    try:
        with open(f"{fname}.txt") as datafile:
            data = list(datafile)
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
        return []
    return data


def easy(data: list[str]) -> int:
    """Easy problem of the day."""
    return 0


def hard(data: list[str]) -> int:
    """Hard problem of the day."""
    return 0


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(realdata))
    print("  solution 2:", hard(realdata))
