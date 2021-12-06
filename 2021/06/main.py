from typing import List
from utils import read_input


def fish_simulation(n_days: int, initial_fish: List[int]) -> int:
    # Initialize list of zeros, from 0 to 9 (max counter)
    days_counter = [0] * 9
    # Update days counter for initial fish
    for fish in initial_fish:
        days_counter[fish] += 1
    for i in range(n_days):
        # Define current day (cyclic)
        current_day = i % 9
        # Define spawning day for adults
        spawn_day = (current_day + 7) % 9
        # Fetch the number of fish creating today
        creators = days_counter[current_day]
        # Update counter
        days_counter[spawn_day] += creators

    return sum(days_counter)


def main():
    input_file = list(map(int, read_input("2021/06/input.txt")[0].split(",")))

    total_days = 80
    print(f"Result of part 1: {fish_simulation(total_days, input_file)}")

    total_days = 256
    print(f"Result of part 2: {fish_simulation(total_days, input_file)}")


if __name__ == "__main__":
    main()
