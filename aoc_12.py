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

    def __init__(self, fname: str, special: Union[str, None] = None,
                 showpaths=False):
        """Initialize maze."""
        self.showpaths = showpaths
        self.connections = Counter()
        self.bigrooms = defaultdict(list)
        with open(f"{fname}.txt") as datafile:
            data = list(datafile)
        self.special = special
        self.read(data)
        self.start = "start"
        self.end = "end"
        self.graph = None
        if self.DEBUG:
            self.debug()

    def read(self, data: list[str]):
        """Read data from input file into maze attributes."""
        for line in data:
            a, b = sorted(line.strip().split('-'))
            if a == a.upper():
                self.bigrooms[a].append(b)
                if b == self.special:
                    self.bigrooms[a].append(self.special + '2')
            else:
                self.connections[(a, b)] += 1
                if a == self.special:
                    self.connections[(self.special + '2', b)] += 1
                elif b == self.special:
                    self.connections[(a, self.special + '2')] += 1

    def debug(self):
        """Print debugging information."""
        print("connections:\n", self.connections)
        print("big rooms:\n", self.bigrooms)

    def prepare_graph(self):
        """Replace big rooms by direct connections between small rooms."""
        for bigroom in self.bigrooms:
            for (a, b) in combinations(self.bigrooms[bigroom], 2):
                self.connections[tuple(sorted((a, b)))] += 1
            if self.DEBUG:
                print("processed", bigroom)
        self.bigrooms = {}
        self.graph = nx.Graph()
        if self.DEBUG:
            self.debug()

    def solve(self) -> int:
        """Solve the maze."""
        self.prepare_graph()
        return self.count_paths()

    def count_paths(self) -> int:
        """Return number of paths in graph."""
        self.graph.add_weighted_edges_from((a, b, self.connections[(a, b)])
                                           for (a, b) in self.connections)
        paths = nx.all_simple_paths(self.graph, self.start, self.end)
        n_paths = 0
        for path in map(nx.utils.pairwise, paths):
            path = list(path)
            if self.special is not None:
                nodes = [node for (node, _) in path]
                if self.special not in nodes:
                    continue
                if self.special + '2' not in nodes:
                    continue
                if nodes.index(self.special + '2') < nodes.index(self.special):
                    continue
            n_path = 1
            if self.showpaths:
                print(list(path))
            for edge in path:
                if self.DEBUG:
                    print(edge, self.graph.edges[edge]["weight"])
                n_path *= self.graph.edges[edge]["weight"]
            n_paths += n_path
        if self.showpaths:
            print("total paths with special", self.special, n_paths)
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
    DEBUG = False
    basic_maze = Maze(fname)
    smallrooms = basic_maze.get_smallrooms()
    n_paths = Maze(fname, showpaths=DEBUG).solve()
    for smallroom in smallrooms:
        if DEBUG:
            print(f"-- doubling {smallroom} --")
        n_paths += Maze(fname, special=smallroom, showpaths=DEBUG).solve()
    return n_paths


if __name__ == "__main__":
    print("PART I")
    print("hintdata 1:", Maze(f"hintdata{DAY}").solve())
    print("hintdata 2:", Maze(f"hintdata{DAY}b").solve())
    print("hintdata 3:", Maze(f"hintdata{DAY}c").solve())
    print("real data :", Maze(f"input{DAY}").solve())
    print("\nPART II")
    print("hintdata 1:", part2(f"hintdata{DAY}"))
    print("hintdata 2:", part2(f"hintdata{DAY}b"))
    print("hintdata 3:", part2(f"hintdata{DAY}c"))
    print("real data :", part2(f"input{DAY}"))
