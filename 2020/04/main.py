import re
from typing import Dict

from utils import read_input_batch


class Passport:
    """Class for Passport entries"""

    def __init__(self, init_dict: Dict = {}):
        # Raise Exception if you don't provide a dict
        if not isinstance(init_dict, Dict):
            raise Exception(
                "Passport needs a initialization dict"
                f" -- you provided a {type(init_dict)}"
            )

        self.init_dict = init_dict

        self.byr = init_dict.get("byr", None)
        self.iyr = init_dict.get("iyr", None)
        self.eyr = init_dict.get("eyr", None)
        self.hgt = init_dict.get("hgt", None)
        self.hcl = init_dict.get("hcl", None)
        self.ecl = init_dict.get("ecl", None)
        self.pid = init_dict.get("pid", None)

        self.valid_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    def is_valid(self):
        # Is the passport valid?
        return not self.valid_keys.difference(self.init_dict.keys())

    def is_byr_valid(self):
        # Is the birth year valid?
        byr = int(self.byr) if self.byr else 0
        return 1920 <= byr <= 2002

    def is_iyr_valid(self):
        # Is the issue year valid?
        iyr = int(self.iyr) if self.iyr else 0
        return 2010 <= iyr <= 2020

    def is_eyr_valid(self):
        # Is the expiration year valid?
        eyr = int(self.eyr) if self.eyr else 0
        return 2020 <= eyr <= 2030

    def is_hgt_valid(self):
        # Is the height valid?
        if self.hgt:
            # Look for specific pattern -- digits + 2 chars
            pattern = re.match(r"^(\d+)([a-z]{2})$", self.hgt)
            if pattern:
                hgt, unit = pattern.groups()
                if unit == "cm":
                    return 150 <= int(hgt) <= 193
                elif unit == "in":
                    return 59 <= int(hgt) <= 76
                else:
                    return False
            else:
                return False
        else:
            return False

    def is_hcl_valid(self):
        # Is hair-color valid?
        return bool(re.match(r"^#\w{6}$", self.hcl)) if self.hcl else False

    def is_ecl_valid(self):
        # Is eye-color valid
        if self.ecl:
            valid_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
            p = re.compile(r"^\w{3}$")
            match = p.search(self.ecl)
            return match.group() in valid_colors if match else False
        else:
            return False

    def is_pid_valid(self):
        # Is passport ID valid?
        return bool(re.match(r"^\d{9}$", self.pid)) if self.pid else False

    def is_complete(self):
        # Are all the tests True?
        return all(
            [
                self.is_byr_valid(),
                self.is_iyr_valid(),
                self.is_eyr_valid(),
                self.is_hgt_valid(),
                self.is_hcl_valid(),
                self.is_ecl_valid(),
                self.is_pid_valid(),
            ]
        )


def main():
    input_file = read_input_batch("2020/04/input.txt")
    # Convert input file into a list of Passports
    passport_list = [
        Passport(dict([re.match(r"(\w+):(.+)", entry).groups() for entry in batch]))
        for batch in input_file
    ]
    #  Obtain the mask of valid passports
    valid = [passport.is_valid() for passport in passport_list]
    print(f"Result of part 1: {sum(valid)}")
    #  Obtain the mask of complete passports
    valid = [passport.is_complete() for passport in passport_list]
    print(f"Result of part 2: {sum(valid)}")


if __name__ == "__main__":
    main()
