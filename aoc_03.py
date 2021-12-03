"""
Advent of Code - tentative pour J3.

Pas le temps de faire du code "propre" aujourd'hui, donc c'est des premiers
jets pas très élégants mais qui font le boulot.

Daniel Kessler (aka Dalker), le 2021.12.03
"""

DAY = "03"
HINTDATA = ["00100", "11110", "10110", "10111", "10101", "01111", "00111",
            "11100", "10000", "11001", "00010", "01010"]


def get_data(day) -> list[str]:
    """Read the day's input file and return contents as a list of ints."""
    with open(f"input{day}.txt") as datafile:
        data = [line for line in datafile]
    return data


def easy(data: list[str]) -> int:
    """Solve day's easy problem."""
    gamma, epsilon = "", ""
    for index in range(len(data[0].strip())):
        ones = 0
        zeros = 0
        for datum in data:
            if datum[index] == "0":
                zeros += 1
            elif datum[index] == "1":
                ones += 1
            else:
                print("problem with", datum, index, end=" ")
        if ones > zeros:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    gamma = int(gamma, 2)
    epsilon = int(epsilon, 2)
    return gamma * epsilon


def oxygen(data: list[str], bit=0, co2=False) -> str:
    """Find oxygen datum."""
    if len(data) == 1:
        return int(data[0], 2)
    n_ones, n_zeros = 0, 0
    d_ones, d_zeros = [], []
    for datum in data:
        if datum[bit] == "0":
            n_zeros += 1
            d_zeros.append(datum)
        elif datum[bit] == "1":
            n_ones += 1
            d_ones.append(datum)
        else:
            print("problem", datum, bit)
    if co2:
        kept = d_ones if n_ones >= n_zeros else d_zeros
    else:
        kept = d_zeros if n_zeros <= n_ones else d_ones
    return oxygen(kept, bit+1, co2)


def hard(data: list[str]) -> int:
    """Solve day's hard problem."""
    return oxygen(data) * oxygen(data, co2=True)


if __name__ == "__main__":
    data = get_data(DAY)
    print("check hint 1:", easy(HINTDATA))  # 22 * 9 = 198
    print("check hint 2:", hard(HINTDATA))
    print("  solution 1:", easy(data))
    print("  solution 2:", hard(data))
