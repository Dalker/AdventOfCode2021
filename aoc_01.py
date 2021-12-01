"""
Advent of Code - tentative pour J1.

NB: this first day is very verbose and full of variants, as I am getting my
bearings around the Advent of Code, to which I am participating for the first
time.

Daniel Kessler (aka Dalker), le 2021.12.01
"""


def count_increases(measurements: list) -> int:
    """Count number of increases between consecutive measurements."""
    current = measurements[0]
    increases = 0
    for measurement in measurements[1:]:
        if measurement > current:
            increases += 1
        current = measurement
    return increases


def count_sliding_increases(measurements: list) -> int:
    """Count number of increases for a between consecutive sliding windows."""
    windows = [sum(measurements[j:j+3]) for j in range(len(measurements) - 2)]
    current = windows[0]
    increases = 0
    for window in windows[1:]:
        if window > current:
            increases += 1
        current = window
    return increases


def count_sliding_increases_improved(measurements: list) -> int:
    """Peaufinage de la fonction d'avant, après avoir rendu le résultat."""
    # objectif: m'habituer plus à la mentalité "programmation fonctionnelle"
    # pour écrire directement ce genre de versions plus courtes et tout autant
    # voire plus efficaces
    windows = [sum(measurements[j:j+3]) for j in range(len(measurements) - 2)]
    return sum(1 if a > b else 0 for a, b in zip(windows[1:], windows[:-1]))


def get_data() -> list:
    """Read day's input."""
    data = []
    with open("input01.txt") as datafile:
        for line in datafile:
            data.append(int(line))
    return data


def get_data_improved() -> list:
    """Maybe this can also be made in a more "functional" style."""
    with open("input01.txt") as datafile:
        data = [int(line) for line in datafile]
    return data


if __name__ == "__main__":
    hint_data = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    measured = get_data_improved()
    print("check hint 1:", count_increases(hint_data))
    print("check hint 2:", count_sliding_increases(hint_data))
    print("solution 1:", count_increases(measured))
    print("solution 2:", count_sliding_increases(measured))
    print("solution 2 (variant):", count_sliding_increases_improved(measured))
