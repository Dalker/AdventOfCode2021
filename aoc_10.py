"""
Advent of Code - tentative pour J10.

Daniel Kessler (aka Dalker), le 2021.12.10
"""

DAY = "10"


OPENERS = {"(": ")", "[": "]", "{": "}", "<": ">"}
CLOSERS = (")", "]", "}", ">")
VALUES = {")": 3, "]": 57, "}": 1197, ">": 25137}
IVALUES = {"(": 1, "[": 2, "{": 3, "<": 4}


def get_data(fname: str) -> list[str]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = list(datafile)
    return data


def syntax_score(line: str) -> tuple[int, bool]:
    """
    Determine syntax score of line.

    This is the value of the first illegal character (wrong closing
    delimiter) or zero.
    """
    stack = []
    for char in line:
        if char in OPENERS:
            stack.append(char)
        elif char in CLOSERS:
            opener = stack.pop()
            if char != OPENERS[opener]:
                return VALUES[char], True
    score = 0
    for opener in reversed(stack):
        score = 5*score + IVALUES[opener]
    return score, False


def solve(data: list[str], part2: bool = False) -> int:
    """Solve problem of the day."""
    corrupted = 0
    incomplete = []
    for line in data:
        score, flag = syntax_score(line)
        if flag:
            corrupted += score
        else:
            incomplete.append(score)
    return corrupted, sorted(incomplete)[len(incomplete) // 2]


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint:", solve(hintdata))
    print("  solution:", solve(realdata))
