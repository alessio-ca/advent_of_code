from utils import read_input
import heapq
import numpy as np

     
def find_max_joltage(banks: list[str], n_batteries: int) -> list[int]:
    max_joltages = []
    for bank in banks:
        array = np.array([int(x) for x in bank], dtype=int)
        n = len(array) - n_batteries + 1
        idx = 0
        indexes: list[int] = []
        while (len(indexes) < n_batteries):
            idx += int(np.argmax(array[idx:n]))
            indexes.append(idx)
            n += 1
            idx += 1
        max_joltages.append(int(''.join(str(x) for x in array[indexes])))
            
        
    return max_joltages

def main(filename: str):
    banks = read_input(filename)
    print(f"Result of part 1: {sum(find_max_joltage(banks,2))}")
    print(f"Result of part 2: {sum(find_max_joltage(banks,12))}")

if __name__ == "__main__":
    main("2025/03/input.txt")
