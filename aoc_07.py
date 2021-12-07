"""
Advent of Code - tentative pour J7.

Daniel Kessler (aka Dalker), le 2021.12.
"""

DAY = "07"
HINTDATA = "16,1,2,0,4,2,7,1,2,14"


def get_data(fname: str) -> str:
    """Read the day's input and return contents in adequate data structure."""
    try:
        with open(f"{fname}.txt") as datafile:
            data = datafile.read()
    except FileNotFoundError:
        print("Day's data file not found. Using Hint Data instead.")
        return []
    return data


def easy(data: list[str]) -> int:
    """Easy problem of the day."""
    data = [int(n) for n in data.strip().split(",")]
    costs = [0] * (max(data) + 1)
    for final_position, _ in enumerate(costs):
        cost = 0
        for datum in data:
            cost += abs(final_position - datum)
        costs[final_position] = cost
    return min(zip(costs, range(max(data) + 1)))


def hard(data: list[str]) -> int:
    """Hard problem of the day."""
    data = [int(n) for n in data.strip().split(",")]
    costs = [0] * (max(data) + 1)
    for final_position, _ in enumerate(costs):
        cost = 0
        for datum in data:
            distance = abs(final_position - datum)
            cost += (distance * (distance+1)) // 2
        costs[final_position] = cost
    return min(zip(costs, range(max(data) + 1)))


if __name__ == "__main__":
    hintdata = HINTDATA
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", easy(hintdata))
    print("check hint 2:", hard(hintdata))
    print("  solution 1:", easy(realdata))
    print("  solution 2:", hard(realdata))
