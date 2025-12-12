from utils import read_input
from collections import defaultdict, deque

def topological_sort(nodes: dict[str, set[str]]) -> list[str]:
    """Perform a topological sort on the directed graph represented by nodes."""

    in_degree: defaultdict[str, int] = defaultdict(int)
    for node, neighbors in nodes.items():
        for neighbor in neighbors:
            in_degree[neighbor] += 1
        if node not in in_degree:
            in_degree[node] = 0

    queue = deque([node for node in nodes if in_degree[node] == 0])
    sorted_list = []

    while queue:
        current = queue.popleft()
        sorted_list.append(current)
        for neighbor in nodes.get(current, []):
            if not neighbor:
                continue
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    
    return sorted_list

def calculate_number_of_paths(nodes: dict[str, set[str]], sort: list[str], start: str, end: str) -> int:
    """Calculate the number of distinct paths from start to end in the given graph."""
    dp = {node: 0 for node in sort}
    dp[start] = 1
    for node in sort:
        for neighbor in nodes[node]:
            dp[neighbor] += dp[node]
    return dp[end]

def main(filename: str):
    data = read_input(filename)
    keys = [line.split(": ")[0] for line in data]
    values = [set(line.split(": ")[1].split(' ')) for line in data]
    nodes = dict(zip(keys, values))
    nodes['out'] = set()

    sort = topological_sort(nodes)
    print(f"Result of part 1: {calculate_number_of_paths(nodes, sort, 'you', 'out')}")
    if 'example' in filename:
        data = read_input(filename.replace('example', 'example_1'))
        keys = [line.split(": ")[0] for line in data]
        values = [set(line.split(": ")[1].split(' ')) for line in data]
        nodes = dict(zip(keys, values))
        nodes['out'] = set()
        sort = topological_sort(nodes)


    total = (
        calculate_number_of_paths(nodes, sort, 'svr', 'fft')
        *calculate_number_of_paths(nodes, sort, 'fft', 'dac')
        *calculate_number_of_paths(nodes, sort, 'dac', 'out')
    )
    print(f"Result of part 2: {total}")
if __name__ == "__main__":
    main("2025/11/input.txt")
