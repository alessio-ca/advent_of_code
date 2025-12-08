from utils import read_input
import numpy as np

    
def main(filename: str):
    data = read_input(filename)
    problems = np.array([list(map(int, line.split())) for line in data[:-1]], dtype=np.int64)
    operations = np.array(list(map(lambda x: 1 if x == '*' else 0, data[-1].split())), dtype=np.int64) 
    total = np.zeros(len(operations), dtype=np.int64)
    total[operations == 0] = problems[:, operations == 0].sum(axis=0)
    total[operations == 1] = problems[:, operations == 1].prod(axis=0)
    print(f"Result of part 1: {total.sum()}")

    data_2 = read_input(filename, line_strip=False)
    columns = np.array([list(map(str, line)) for line in data_2[:-1]], dtype=str).T
    is_delimiter = (columns == ' ').all(axis=1)
    problems_2 = []
    digits = []
    for idx, row in enumerate(columns):
        if not is_delimiter[idx]:
            digits.append(''.join(row))
        else:
            problems_2.append(list(map(int, digits)))
            digits = []
    problems_2.append(list(map(int, digits)))  # append last batch
    total_2 = 0
    for op, problem in zip(operations, problems_2):
        if op == 0:
            total_2 += int(np.sum(problem))
        else:
            total_2 += int(np.prod(problem))

    print(f"Result of part 2: {total_2}")
    

if __name__ == "__main__":
    main("2025/06/input.txt")
