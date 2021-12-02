"""
Advent of Code - tentative pour J.

Daniel Kessler (aka Dalker), le 2021.12.
"""

DAY = "01"
HINTDATA = []


def get_data(day) -> list[str]:
    """Read the day's input file and return contents as a list of ints."""
    with open(f"input{day}.txt") as datafile:
        data = [line for line in datafile]
    return data


if __name__ == "__main__":
    data = get_data(DAY)
    print("check hint 1:", )
    print("check hint 2:", )
    print("  solution 1:", )
    print("  solution 2:", )
