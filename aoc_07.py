"""
Advent of Code - tentative pour J7.

Daniel Kessler (aka Dalker), le 2021.12.07
"""

DAY = "07"
HINTDATA = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def get_data(fname: str) -> list[int]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = [int(n) for n in datafile.read().strip().split(",")]
    return data


def solve(data: list[int], part2: bool = False) -> tuple[int, int]:
    """Solution for both problems of the day."""
    costs = [0] * (max(data) + 1)
    for final_position, _ in enumerate(costs):
        cost = 0
        for datum in data:
            if not part2:
                cost += abs(final_position - datum)
            else:
                distance = abs(final_position - datum)
                cost += (distance * (distance+1)) // 2
        costs[final_position] = cost
    return min(zip(costs, range(max(data) + 1)))


if __name__ == "__main__":
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(HINTDATA))
    print("check hint 2:", solve(HINTDATA, part2=True))
    print("  solution 1:", solve(realdata))
    print("  solution 2:", solve(realdata, part2=True))
