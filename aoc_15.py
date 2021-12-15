"""
Advent of Code - tentative pour J15.

Daniel Kessler (aka Dalker), le 2021.12.15
"""

from itertools import product
from queue import PriorityQueue

Coords = tuple[int, int]
Costs = dict[Coords, int]

DAY = "15"


def get_data(fname: str) -> tuple[int, Costs]:
    """Read the day's input and return contents in adequate data structure."""
    costs = {}
    with open(f"{fname}.txt") as datafile:
        data = list(datafile)
    size = len(data)
    for row, line in enumerate(data):
        for col, value in enumerate(line.strip()):
            costs[(col, row)] = int(value)
    return size, costs


def neighbours(xy: Coords, size: int) -> list[Coords]:
    """Return viable neighbours in a square grid."""
    # pylint: disable=invalid-name
    x, y = xy
    res = []
    for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
        if 0 <= x+dx < size and 0 <= y+dy < size:
            res.append((x+dx, y+dy))
    return res


def increase_maze(size: int, costs: Costs) -> tuple[int, Costs]:
    """Increase size of maze for part 2."""
    # pylint: disable=invalid-name
    new_costs = {}
    for x, y in costs:
        cost = costs[(x, y)]
        for dx, dy in product(range(5), range(5)):
            new_costs[(x + size*dx,
                       y + size*dy)] = (cost - 1 + dx + dy) % 9 + 1
    return 5*size, new_costs


def solve(data: tuple[int, Costs], part2: bool = False) -> int:
    """Solve problem of the day - seems like an A* will do."""
    size, entrance_cost = data
    if part2:
        size, entrance_cost = increase_maze(size, entrance_cost)
    goal = (size - 1, size - 1)
    queue: PriorityQueue[tuple[int, Coords]] = PriorityQueue()
    # predecessor = {(0, 0): None}  # <-- for showing path (not implemented)
    reaching_cost = {(0, 0): 0}
    queue.put((2*size, (0, 0)))  # cost, (x, y)
    # steps = 0  # <-- for checking efficiency
    while True:
        _, current = queue.get()
        cost = reaching_cost[current]
        if current == goal:
            # print(steps, "steps done")
            return cost
        for neighbour in neighbours(current, size):
            new_cost = cost + entrance_cost[neighbour]
            if (neighbour not in reaching_cost
                    or new_cost < reaching_cost[neighbour]):
                # next line means Manhattan distance: surprisingly inefficient!
                # distance = 2*size - neighbour[0] - neighbour[1]
                distance = 0  # means Dijkstra: surprisingly efficient here!
                # steps += 1
                # predecessor[neighbour] = current
                reaching_cost[neighbour] = new_cost
                queue.put((new_cost + distance, neighbour))


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(hintdata))
    print("  solution 1:", solve(realdata))
    print("check hint 2:", solve(hintdata, part2=True))
    print("  solution 2:", solve(realdata, part2=True))
