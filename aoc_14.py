"""
Advent of Code - tentative pour J14.

Daniel Kessler (aka Dalker), le 2021.12.14
"""

import cProfile
from time import process_time
import tracemalloc
from collections import Counter  # , deque

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


def count_chain(chain: str) -> int:
    """Count difference between most and least frequent letter."""
    counts: dict[str, int] = Counter()
    for char in chain:
        counts[char] += 1
    printcount(counts)
    max_count = max(counts[c] for c in counts)
    min_count = min(counts[c] for c in counts)
    return max_count - min_count


def solve(base: str, rules: dict[str, str], steps=10) -> int:
    """Solve problem of the day."""
    chain = base
    for _ in range(steps):
        chain = advance(chain, rules)
    return count_chain(chain)


def solve2(base: str, rules: dict[str, str], steps=10) -> int:
    """Solve problem of the day in a smarter way (using a lot less memory)."""
    counts: dict[str, int] = Counter()
    # essayé avec deque et list en profilant - pas de grande différence
    # et pour deque avec popleft/appendleft et pop/append - idem
    rest = list((char, steps) for char in base)
    char, level = rest.pop()
    while rest:
        newchar = rules[rest[-1][0] + char]
        if level == 1:
            counts[char] += 1
            counts[newchar] += 1
            char, level = rest.pop()
        else:
            level -= 1
            rest.append((newchar, level))
    counts[char] += 1
    printcount(counts)
    return max(counts.values()) - min(counts.values())


def solve3_recur(pair: str, rules: dict[str, str], count, steps: int):
    """Recursively count characters."""
    if steps == 0:
        count[pair[0]] += 1
    else:
        a, b = pair
        newchar = rules[pair]
        solve3_recur(a+newchar, rules, count, steps-1)
        solve3_recur(newchar+b, rules, count, steps-1)


def solve3(base: str, rules: dict[str, str], steps=10) -> int:
    """Solver based on Sébastien's hint on Discord."""
    count = Counter()
    for a, b in zip(base[:-1], base[1:]):
        solve3_recur(a+b, rules, count, steps)
    count[base[-1]] += 1
    printcount(count)
    return max(count.values()) - min(count.values())


class Profiler:
    """Profiler for process time and memory usage."""

    def __init__(self):
        self.time = process_time()
        tracemalloc.start()

    def stamp(self):
        """Print process time and peak mem usage since creation."""
        newtime = process_time()
        print(" --> time (ms):", round(1000*(newtime - self.time)),
              "-- peak mem (kB)",
              round(tracemalloc.get_traced_memory()[1] / 1000, 1))
        self.time = newtime
        tracemalloc.reset_peak()


def printcount(count: dict[str, int]):
    """Print a Counter in sorted order, for debugging purposes."""
    return  # deactivate this for now
    print(" <", end="")
    print(", ".join([str(key) + ": " + str(count[key])
                     for key in sorted(count)]), end=">\n")


def test(name: str, solver, data: tuple, steps: int):
    """Profile a given solver on a given dataset."""
    print("* ", name, end=" ")
    print("solution:", solver(*data, steps), end=" ")
    profile.stamp()


if __name__ == "__main__":
    profile = Profiler()
    hintdata = get_data(f"hintdata{DAY}")
    realdata = get_data(f"input{DAY}")
    test("  hint, solver 1", solve, hintdata, 10)
    test("  hint, solver 2", solve2, hintdata, 10)
    test("  hint, solver 3", solve3, hintdata, 10)
    test("part 1, solver 1", solve, realdata, 10)
    test("part 1, solver 2", solve2, realdata, 10)
    test("part 1, solver 3", solve3, realdata, 10)
    test("part ?, solver 1", solve, realdata, 15)
    test("part ?, solver 2", solve2, realdata, 15)
    test("part ?, solver 3", solve3, realdata, 15)
    with cProfile.Profile() as profiler:
        solve2(*realdata, 15)
    profiler.print_stats()
