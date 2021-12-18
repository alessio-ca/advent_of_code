from utils import read_input
import re
from typing import List


class Area:
    def __init__(self, bounds: List[int]):
        if len(bounds) != 4:
            raise ValueError
        self.x_min, self.x_max, self.y_min, self.y_max = bounds

    def simulate(self, vx, vy):
        x, y = 0, 0

        while y >= self.y_min:
            x += vx
            y += vy
            vx -= int(vx > 0)
            vy -= 1

            if (self.x_min <= x <= self.x_max) and (self.y_min <= y <= self.y_max):
                return 1

        return 0


def main():
    input_file = read_input("2021/17/input.txt")[0]
    area = Area(list(map(int, re.findall(r"[-\d]+", input_file))))

    print(f"Result of part 1: {area.y_min * (area.y_min + 1) // 2}")

    count = 0
    for i in range(1, area.x_max + 1):
        for j in range(area.y_min, -area.y_min + 1):
            vx, vy = i, j
            count += area.simulate(vx, vy)

    print(f"Result of part 2: {count}")


if __name__ == "__main__":
    main()
