"""
Advent of Code - tentative pour J<n>.

Daniel Kessler (aka Dalker), le 2021.12.<n>
"""

DAY = "<n>"


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = list(datafile)
    return data


def solve(data: list[str], part2: bool = False) -> int:
    """Solve problem of the day."""
    return 0


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(hintdata))
    # print("  solution 1:", solve(realdata))
    # print("check hint 2:", solve(hintdata, part2=True))
    # print("  solution 2:", solve(realdata, part2=True))
