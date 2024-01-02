from utils import read_input
import numpy as np


class CPU:
    def __init__(self) -> None:
        self.X = 1
        self.idx_s = 0
        self.cycle = 1
        self.strenghts = list(range(20, 300, 40))
        self.res = []
        self.crt = []

    def update_res(self):
        self.cycle += 1
        # Check if cycle syncs with the current strength to measure
        if self.cycle == self.strenghts[self.idx_s]:
            self.res.append(self.strenghts[self.idx_s] * self.X)
            self.idx_s += 1
        # Exit after 240 cycle
        if self.cycle > 240:
            raise StopIteration

    def draw_crt(self):
        # Measure screen pos as the cycle number modulo 40
        screen_pos = (self.cycle - 1) % 40
        # Check if the relative difference between the register and the screen pos is
        #  less or equal to 1
        if abs(self.X - screen_pos) <= 1:
            self.crt.append("#")
        else:
            self.crt.append(".")


def main(filename: str):
    instructions = read_input(filename, line_strip=True)
    cpu = CPU()

    for line in instructions:
        # Perform instruction
        try:
            cpu.draw_crt()
            cpu.update_res()
            # If the line doesn't start with "n", it's an addx command
            if line[0] != "n":
                cpu.draw_crt()
                _, num = line.split(" ")
                cpu.X += int(num)
                cpu.update_res()

        except StopIteration:
            break

    print(f"Result of part 1: {sum(cpu.res)}")

    image = np.array(cpu.crt).reshape(6, 40)
    decoded = ""
    for row in image:
        decoded += "".join(row) + "\n"

    print("Result of part 2: ")
    print("")
    print(f"{decoded}")


if __name__ == "__main__":
    main("2022/10/input.txt")
