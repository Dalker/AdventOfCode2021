"""
Advent of Code - tentative pour J8.

Daniel Kessler (aka Dalker), le 2021.12.08
"""

from collections import defaultdict

DAY = "08"


def get_data(fname: str) -> list[list[list[str]]]:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = [[part.split(" ")
                 for part in line.strip().split(" | ")]
                for line in datafile]
    return data


def solve(data: list[list[list[str]]]) -> int:
    """Solve problem of the day."""
    unique = 0
    for line in data:
        _, output = line
        for digit in output:
            if len(digit) in (2, 3, 4, 7):
                unique += 1
    return unique


def unentangle(codes: list[str]) -> list[set]:
    """Find what each wire really means."""
    LENGTH2DIGIT = {2: 1, 3: 7, 4: 4, 7: 8}
    digit2code: list[set] = [set()]*10
    # wiring = {}
    bylength = defaultdict(list)
    for rawcode in codes:
        code = set(rawcode)
        n_segments = len(code)
        bylength[n_segments].append(code)
        if n_segments in LENGTH2DIGIT:
            digit2code[LENGTH2DIGIT[n_segments]] = code
    for code in bylength[6]:
        if digit2code[1].difference(code):
            digit2code[6] = code
        elif not digit2code[4].difference(code):
            digit2code[9] = code
        else:
            digit2code[0] = code
    for code in bylength[5]:
        if not digit2code[1].difference(code):
            digit2code[3] = code
        elif len(digit2code[4].difference(code)) == 2:
            digit2code[2] = code
        else:
            digit2code[5] = code
    return digit2code


def solve2(data: list[list[list[str]]]) -> int:
    """Solve second problem of the day."""
    total = 0
    for line in data:
        digits, output = line
        decoder = unentangle(digits)
        value = 0
        for code in output:
            value += [n for n in range(10) if decoder[n] == set(code)][0]
            value *= 10
        total += value//10
    return total


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(hintdata))
    print("check hint 2:", solve2(hintdata))
    print("  solution 1:", solve(realdata))
    print("  solution 2:", solve2(realdata))
