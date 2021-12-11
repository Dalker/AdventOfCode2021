"""
Advent of Code - tentative pour J11.

Daniel Kessler (aka Dalker), le 2021.12.11
"""
from itertools import product
from copy import deepcopy

import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
import matplotlib.animation  as anim

DAY = "11"


def step(energies: npt.NDArray[int]) -> npt.NDArray[int]:
    """Perform one step of dumbo octopus evolution."""
    m, n = energies.shape
    # first,  increase each octopus' energy by 1
    for i, j in product(range(m), range(n)):
        energies[i, j] += 1
    # the flash as much as possible
    while any(energy > 9 for energy in energies.flatten()):
        for x, y in product(range(m), range(n)):
            if energies[x, y] > 9:
                energies[x, y] = 0
                # NB ci-dessous: [0, 0] ne pose pas de souci vu la vérif != 0
                for dx, dy in product([-1, 0, 1], [-1, 0, 1]):
                    # mon try...except causait plus de bugs qu'autre chose
                    # donc je change pour une vérification d'intervalle
                    if 0 <= x+dx < m and 0 <= y+dy < n:
                        # on est dans la grille, on peut vérifier la valeur
                        if energies[x+dx, y+dy] != 0:
                            energies[x+dx, y+dy] += 1


def solve(octopi: npt.NDArray[int]) -> int:
    """Solve problem of the day."""
    flashes = 0
    for n in range(100):
        # print(f"step {n}")
        # print(octopi)
        step(octopi)
        flashes += sum([octopus == 0 for octopus in octopi.flatten()])
    return flashes


def solve2(octopi: npt.NDArray[int]) -> int:
    """Solve second part."""
    dim_x, dim_y = octopi.shape
    for n in range(1000):
        step(octopi)
        if all(octopi[i, j] == octopi[0, 0]
               for (i, j) in product(range(dim_x), range(dim_y))):
            return n+1
    return -1


def step_anim(grid, image):
    """Avancer l'animation d'un frame."""
    step(grid)
    image.set_data(grid)
    # retourner une colleciton d'"artistes" qu'il faut mettre à jour
    return image,


def visualize(octopi: npt.NDArray[int]):
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
    # visualize(hintdata)
    # visualize(realdata)
