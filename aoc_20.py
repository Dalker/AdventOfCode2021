"""
Advent of Code - tentative pour J20.

Daniel Kessler (aka Dalker), le 2021.12.20
"""

from itertools import product
from typing import Callable

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt

Map = npt.NDArray[str]


def get_data(fname: str) -> tuple[str, Map]:
    """Read the day's input and return contents in adequate data structure."""
    decoder = ""
    image = []
    with open(fname) as datafile:
        while True:
            line = datafile.readline().strip()
            if line == "":
                break
            decoder += ''.join(['0' if char == '.' else '1'
                                for char in line])
        for line in datafile:
            image += [list('0' if char == '.' else '1'
                           for char in line.strip())]
    return decoder, np.array(image)


def get_decode() -> Callable:
    """Closure for iteratively decoding an image."""
    padder = "0"

    def decode(decoder: str, image: Map) -> Map:
        """Perform one step of padding and decoding image."""
        nonlocal padder
        image = np.pad(image, 10, constant_values=padder)
        new_image = np.full(image.shape, padder)
        for row, col in product(range(2, image.shape[0]-2),
                                range(2, image.shape[1]-2)):
            stamp = image[row:row+3, col:col+3]
            code = int("".join(stamp.flatten()), 2)
            # ascii_print(stamp)
            # print(code)
            new_image[row+1, col+1] = decoder[code]
        new_image = new_image[3:-3, 3:-3]
        padder = new_image[0, 0]
        return new_image[6:-6, 6:-6]
    return decode


def ascii_print(image: Map) -> None:
    """Print ASCII art representation of map."""
    for line in image:
        print("".join(['.' if char == '0' else '#' for char in line]))


def mp_show(image: Map) -> None:
    """Show image on matplotlib plot."""
    _, ax = plt.subplots()
    ax.matshow(image)
    plt.show()


def solve(decoder: str, image: Map, n_enhancements=2) -> int:
    """Solve problem of the day."""
    decode = get_decode()
    for _ in range(n_enhancements):
        image = decode(decoder, image)
    mp_show(image.astype(int))
    return image.astype(int).sum()


if __name__ == "__main__":
    hintdata = get_data("hintdata20.txt")
    realdata = get_data("input20.txt")
    print("check hint 1:", solve(*hintdata))
    print("  solution 1:", solve(*realdata))  # 6152 is too high
    # 5363 is too high !? (after fiddling with padding)
    # 5155 is wrong.. (not allowed any more "too high" or "too low" apparently)
    print("check hint 2:", solve(*hintdata, 50))
    print("  solution 2:", solve(*realdata, 50))
