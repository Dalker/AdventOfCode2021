"""
Advent of Code - tentative pour J2.

Daniel Kessler (aka Dalker), le 2021.12.02
"""

DAY = "02"
HINTDATA = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]


def get_data(day) -> list[str]:
    """Read the day's input file and return contents as a list of ints."""
    with open(f"input{day}.txt") as datafile:
        data = [line for line in datafile]
    return data


def compute_course(data: list[str]) -> int:
    """Compute submarine course."""
    depth, x_pos = 0, 0
    for line in data:
        command, delta = line.split()
        delta = int(delta)
        if command == "forward":
            x_pos += delta
        elif command == "up":
            depth -= delta
        elif command == "down":
            depth += delta
        else:
            print(command, "command not known")
    return depth * x_pos


def compute_with_aim(data: list[str]) -> int:
    """Compute course again, reinterpreting 'up' and 'down'."""
    aim, depth, x_pos = 0, 0, 0
    for line in data:
        command, delta = line.split()
        delta = int(delta)
        if command == "up":
            aim -= delta
        elif command == "down":
            aim += delta
        elif command == "forward":
            x_pos += delta
            depth += aim*delta
        else:
            print(command, "command not known")
    return depth * x_pos


if __name__ == "__main__":
    data = get_data(DAY)
    print("check hint 1:", compute_course(HINTDATA))
    print("check hint 2:", compute_with_aim(HINTDATA))
    print("  solution 1:", compute_course(data))
    print("  solution 2:", compute_with_aim(data))
