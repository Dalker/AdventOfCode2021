"""
Advent of Code - tentative pour J14.

Daniel Kessler (aka Dalker), le 2021.12.14
"""

from collections import Counter

DAY = "14"


def get_data(fname: str) -> tuple[str, dict[str, str]]:
    """Read the day's input and return contents in adequate data structure."""
    rules = {}
    with open(f"{fname}.txt") as datafile:
        base = datafile.readline().strip()
        datafile.readline()
        for line in datafile:
            pair, insert = line.strip().split(" -> ")
            rules[pair] = insert
    return base, rules


def advance(start: str, rules: dict[str, str]):
    """Perform one step of polymerisation."""
    chain = start[0]
    for a, b in zip(start[:-1], start[1:]):
        chain += rules[a + b] + b
    return chain


def count(chain: str) -> int:
    """Count difference between most and least frequent letter."""
    counts = Counter()
    for char in chain:
        counts[char] += 1
    max_count = max(counts[c] for c in counts)
    min_count = min(counts[c] for c in counts)
    return max_count - min_count


def solve(base: str, rules: dict[str, str], steps=10) -> int:
    """Solve problem of the day."""
    chain = base
    for _ in range(steps):
        chain = advance(chain, rules)
    return count(chain)


if __name__ == "__main__":
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    print("check hint 1:", solve(*hintdata))
    # print("check hint 2:", solve(*hintdata, steps=40))
    print("  solution 1:", solve(*realdata))
    # print("  solution 2:", solve(*realdata, steps=40))
