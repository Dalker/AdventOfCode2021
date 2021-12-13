"""
Advent of Code - tentative pour J13.

Daniel Kessler (aka Dalker), le 2021.12.13
"""

DAY = "13"


def get_data(fname: str) -> tuple[set[tuple[int, int]],
                                  list[tuple[str, int]]]:
    """Read the day's input and return contents in adequate data structure."""
    coords = set()
    instructions = []
    with open(f"{fname}.txt") as datafile:
        for line in datafile:
            if line == "\n":
                break
            coords.add(tuple(int(n)
                             for n in line.strip().split(",")))
        for line in datafile:
            instr = line.split()[-1].split("=")
            instructions.append((instr[0], int(instr[1])))
    return coords, instructions


def read(coords: set[tuple[int, int]]):
    """Read the code."""
    x_max, y_max = max(x for x, y in coords), max(y for x, y in coords)
    for y in range(y_max+1):
        print("".join(["▇" if (x, y) in coords else " "
                       for x in range(x_max+1)]))


def solve(coords: set[tuple[int, int]],
          instructions: list[tuple[str, int]]) -> int:
    """Solve problem of the day."""
    answer1 = 0
    for axis, number in instructions:
        if axis == "x":
            coords = set((x, y) if x < number else (2*number - x, y)
                         for x, y in coords)
        else:
            coords = set((x, y) if y < number else (x, 2*number - y)
                         for x, y in coords)
        if not answer1:
            answer1 = len(coords)
    read(coords)
    return answer1


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("hint part 1:", solve(*hintdata))
    print("solution part 1:", solve(*realdata))
