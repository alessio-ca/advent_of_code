import numpy as np
from scipy.ndimage import convolve

from utils import read_input


class FlashySystem:
    def __init__(self, X: np.ndarray):
        # Define convolution filter
        self.conv_filter = np.ones(shape=(3, 3), dtype=int)
        self.conv_filter[1, 1] = 0
        #  Initialize
        self._reset(X)

    def _reset(self, X: np.ndarray):
        """Reset the system"""
        self.X = X.copy()
        # Initialise flash counter
        self.count_flashes = 0
        # Initialize mask of occurred flashes
        self.mask_past_flashes = np.zeros(shape=self.X.shape, dtype=int)
        # Initialize internal day counter
        self._i = 0

    def _zero_mask(self):
        """Zero the mask of occurred flashes"""
        self.mask_past_flashes[:] = 0
        return self

    def _update_array(self):
        """Update timers"""
        self.X += 1
        return self

    def _flash_loop(self):
        """At each day, simulate flashes"""
        # Create mask for marking the flashing octopuses
        mask_flashing = np.where(self.X > 9, 1, 0)
        # Ignore entries who have already flashed
        mask_flashing[self.mask_past_flashes == 1] = 0
        # Calculate how many flashes there are
        Y = convolve(mask_flashing, self.conv_filter, mode="constant")
        # Add to array
        self.X = self.X + Y
        # Update the mask of past flashes with those flashing this round
        self.mask_past_flashes[mask_flashing == 1] = 1
        # Return the number of occurred flashes
        return Y.sum()

    def check_syncro(self):
        """Check if we reached syncronization"""
        return self.mask_past_flashes.sum() == self.X.shape[0] * self.X.shape[1]

    def run_day(self):
        """Run a single day"""
        # Update array
        self._update_array()
        # Reset the mask
        self._zero_mask()
        # Loop over the flashing events
        while self._flash_loop():
            continue
        # Set the flashing octopuses to 0
        self.X[self.mask_past_flashes == 1] = 0
        # Count the number of flashes
        self.count_flashes += self.mask_past_flashes.sum()

        return self

    def run(self, n_days: int):
        """Run for n_days. If n_days is negative,
        simulate until syncronization is reached"""
        if n_days >= 0:
            # Simulate for n_days
            for i in range(0, n_days):
                self.run_day()
                self._i += 1
        else:
            # Simulate until syncronyzation is achieved
            while not self.check_syncro():
                self.run_day()
                self._i += 1

        return self


def main():
    input_file = read_input("2021/11/input.txt")

    # Create numpy array of the initial grid and initialize system
    X = np.array([[num for num in line] for line in input_file], dtype=int)

    # Create system
    system = FlashySystem(X)
    system.run(100)
    print(f"Result of part 1: {system.count_flashes}")
    system._reset(X)
    system.run(-1)
    print(f"Result of part 2: {system._i}")


if __name__ == "__main__":
    main()
