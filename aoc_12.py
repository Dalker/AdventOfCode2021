"""
Advent of Code - tentative pour J12.

Daniel Kessler (aka Dalker), le 2021.12.12
"""
from typing import Union
from collections import defaultdict, Counter
from itertools import combinations
import networkx as nx

DAY = "12"


class Maze:
    """A combinatorial maze that needs lots of counting."""
    DEBUG = False

    def __init__(self, fname: str, start=None, end=None):
        """Initialize maze."""
        self.connections = Counter()
        self.bigrooms = defaultdict(list)
        with open(f"{fname}.txt") as datafile:
            data = list(datafile)
        self.read(data, start, end)
        if self.DEBUG:
            self.debug()

    def read(self, data: list[str],
             start: Union[str, None], end: Union[str, None]):
        """Read data from input file into maze attributes."""
        for line in data:
            a, b = sorted(line.strip().split('-'))
            if start is not None:
                if "start" in (a, b):
                    continue
                if start == a:
                    a = "start"
                elif start == b:
                    b = "start"
            if end is not None:
                if "end" in (a, b):
                    continue
                if end == a:
                    a = "end"
                elif end == b:
                    b = "end"
            if a == a.upper():
                self.bigrooms[a].append(b)
            else:
                self.connections[(a, b)] += 1

    def debug(self):
        """Print debugging information."""
        print("connections:\n", self.connections)
        print("big rooms:\n", self.bigrooms)

    def process_bigrooms(self):
        """Replace big rooms by direct connections between small rooms."""
        for bigroom in self.bigrooms:
            for (a, b) in combinations(self.bigrooms[bigroom], 2):
                self.connections[tuple(sorted((a, b)))] += 1
            if self.DEBUG:
                print("processed", bigroom)
        self.bigrooms = {}
        if self.DEBUG:
            self.debug()

    def solve(self) -> int:
        """Solve the maze."""
        self.process_bigrooms()  # transform maze into simple network
        self.graph = nx.Graph()
        self.graph.add_weighted_edges_from((a, b, self.connections[(a, b)])
                                           for (a, b) in self.connections)
        paths = nx.all_simple_paths(self.graph, "start", "end")
        n_paths = 0
        for path in map(nx.utils.pairwise, paths):
            n_path = 1
            for edge in path:
                if self.DEBUG:
                    print(edge, self.graph.edges[edge]["weight"])
                n_path *= self.graph.edges[edge]["weight"]
            n_paths += n_path
        return n_paths

    def get_smallrooms(self) -> set[str]:
        """Get set of non-terminal small rooms."""
        smallrooms = set()
        for a, b in self.connections:
            smallrooms.add(a)
            smallrooms.add(b)
        for A in self.bigrooms:
            for a in self.bigrooms[A]:
                smallrooms.add(a)
        smallrooms.remove("start")
        smallrooms.remove("end")
        return smallrooms


def part2(fname: str) -> int:
    """Solve part2 of puzzle."""
    basic_maze = Maze(fname)
    smallrooms = basic_maze.get_smallrooms()
    n_paths = Maze(fname).solve()
    for smallroom in smallrooms:
        n_paths += (Maze(fname, end=smallroom).solve()
                    * Maze(fname, start=smallroom).solve())
    return n_paths


if __name__ == "__main__":
    print("PART I")
    print("hintdata 1:", Maze(f"hintdata{DAY}").solve())
    print("hintdata 2:", Maze(f"hintdata{DAY}b").solve())
    print("hintdata 3:", Maze(f"hintdata{DAY}c").solve())
    print("real data :", Maze(f"input{DAY}").solve())
    print("\nPART II")
    print("hintdata 1:", part2(f"hintdata{DAY}"))
    # print("hintdata 2:", part2(f"hintdata{DAY}b"))
    # print("hintdata 3:", part2(f"hintdata{DAY}c"))
