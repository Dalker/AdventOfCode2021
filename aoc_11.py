"""
Advent of Code - tentative pour J11.

Daniel Kessler (aka Dalker), le 2021.12.11
"""
from itertools import product
from copy import deepcopy

import numpy as np
import numpy.typing as npt
# à l'heure actuelle, matplotlib ne supporte par mypy
import matplotlib.pyplot as plt  # type: ignore
import matplotlib.animation as anim  # type: ignore
from matplotlib.image import AxesImage  # type: ignore

DAY = "11"


def step(energies: npt.NDArray[np.int8]):
    """Perform one step of dumbo octopus evolution."""
    rows, cols = energies.shape
    # first,  increase each octopus' energy by 1
    for i, j in product(range(rows), range(cols)):
        energies[i, j] += 1
    # the flash as much as possible
    while any(energy > 9 for energy in energies.flatten()):
        for row, col in ((r, c) for r, c in product(range(rows), range(cols))
                         if energies[r, c] > 9):
            energies[row, col] = 0
            for neighbour in ((row+drow, col+dcol)
                              for drow, dcol in product([-1, 0, 1], [-1, 0, 1])
                              if 0 <= row+drow < rows
                              and 0 <= col+dcol < cols):
                # on est dans la grille, on peut vérifier la valeur
                # NB: le centre est automatiquement exclu car il a la valeur 0
                if energies[neighbour] != 0:
                    energies[neighbour] += 1


def solve(octopi: npt.NDArray[np.int8]) -> int:
    """Solve problem of the day."""
    flashes = 0
    for _ in range(100):
        # print(f"step {n}")
        # print(octopi)
        step(octopi)
        flashes += sum([octopus == 0 for octopus in octopi.flatten()])
    return flashes


def solve2(octopi: npt.NDArray[np.int8]) -> int:
    """Solve second part."""
    dim_x, dim_y = octopi.shape
    for stage in range(1000):
        step(octopi)
        if all(octopi[i, j] == octopi[0, 0]
               for (i, j) in product(range(dim_x), range(dim_y))):
            return stage + 1
    return -1


def step_anim(grid: npt.NDArray[np.int8], image: AxesImage):
    """Avancer l'animation d'un frame."""
    step(grid)
    image.set_data(grid)
    # retourner une colleciton d'"artistes" qu'il faut mettre à jour
    return (image, )


def visualize(octopi: npt.NDArray[np.int8]):
    """Visualizer 1000 pas de l'automate."""
    fig = plt.figure()
    axes = fig.add_subplot()
    axes.axis("off")
    img = axes.matshow(octopi)
    # NB sur le lambda: FuncAnimation envoie comme argument le numéro de frame,
    # que l'on ignore, et veut en retour une collection d'artistes
    automaton = anim.FuncAnimation(fig,
                                   lambda _: step_anim(octopi, img),
                                   frames=300, blit=True)
    automaton.save("dumbo.gif", fps=10)


if __name__ == "__main__":
    hintdata = np.genfromtxt(f"hintdata{DAY}.txt", dtype=np.int8, delimiter=1)
    realdata = np.genfromtxt(f"input{DAY}.txt", dtype=np.int8, delimiter=1)
    print("check hint 1:", solve(deepcopy(hintdata)))
    print("check hint 2:", solve2(deepcopy(hintdata)))
    print("  solution 1:", solve(deepcopy(realdata)))
    print("  solution 2:", solve2(deepcopy(realdata)))
    # faire au plus une visualisation à la fois (décommenter à choix)
    visualize(hintdata)
    # visualize(realdata)
