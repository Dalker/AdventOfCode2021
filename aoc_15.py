"""
Advent of Code - tentative pour J15.

Daniel Kessler (aka Dalker), le 2021.12.15
"""

from queue import PriorityQueue

DAY = "15"


def get_data(fname: str) -> tuple[int, dict[tuple[int, int], int]]:
    """Read the day's input and return contents in adequate data structure."""
    costs = {}
    with open(f"{fname}.txt") as datafile:
        data = list(datafile)
    size = len(data)
    for y, line in enumerate(data):
        for x, value in enumerate(line.strip()):
            costs[(x, y)] = int(value)
    return size, costs


def neighbours(xy: tuple[int, int], size: int) -> list[tuple[int, int]]:
    """Return viable neighbours in a square grid."""
    x, y = xy
    res = []
    for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        if 0 <= x+dx < size and 0 <= y+dy < size:
            res.append((x+dx, y+dy))
    return res


def solve(data: tuple[int, dict], part2: bool = False) -> int:
    """Solve problem of the day - seems like a A* will do."""
    size, entrance_cost = data
    if part2:
        new_costs = {}
        for x, y in entrance_cost:
            cost = entrance_cost[(x, y)]
            for dx in range(5):
                for dy in range(5):
                    new_costs[(x+size*dx, y+size*dy)] = (cost - 1 + dx + dy)%9 + 1
        size *= 5
        entrance_cost = new_costs
    goal = (size - 1, size - 1)
    queue = PriorityQueue()
    # predecessor = {(0, 0): None}
    reaching_cost = {(0, 0): 0}
    queue.put((2*size, (0, 0)))  # cost, (x, y)
    while True:
        _, current = queue.get()
        cost = reaching_cost[current]
        # print(current, cost)
        if current == goal:
            return cost
        for neighbour in neighbours(current, size):
            if neighbour not in reaching_cost:
                distance = 2*size - neighbour[0] - neighbour[1]
                distance = 0
                reaching_cost[neighbour] = cost + entrance_cost[neighbour]
                queue.put((reaching_cost[neighbour] + distance, neighbour))


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(hintdata))
    print("check hint 2:", solve(hintdata, part2=True))
    print("  solution 1:", solve(realdata))
    print("  solution 2:", solve(realdata, part2=True))
