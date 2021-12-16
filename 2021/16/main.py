from utils import read_input
from typing import Tuple
from functools import reduce


def _decode(string: str) -> Tuple[int, str, int]:
    packet_version, type_id, bits = int(string[:3], 2), int(string[3:6], 2), string[6:]
    if type_id == 4:
        # Take substrings
        repr = ""
        while bits[0] != "0":
            repr, bits = repr + bits[1:5], bits[5:]
        repr, bits = repr + bits[1:5], bits[5:]
        number = int(repr, 2)
        return number, bits, packet_version
    else:
        # This is an operator
        len_type_id, bits = bits[0], bits[1:]
        subpackets = []
        if int(len_type_id):
            # Next 11 bits specify the number of subpackets
            n_subpackets, bits = int(bits[:11], 2), bits[11:]
            for _ in range(n_subpackets):
                # Find subpackets
                subpacket, bits, sub_packet_version = _decode(bits)
                packet_version += sub_packet_version
                subpackets.append(subpacket)
        else:
            # Next 15 bits specify the length of subpackets
            len_subpackets, bits = int(bits[:15], 2), bits[15:]
            first_size = len(bits)
            while (first_size - len(bits)) < len_subpackets:
                # Find subpackets
                subpacket, bits, sub_packet_version = _decode(bits)
                packet_version += sub_packet_version
                subpackets.append(subpacket)

        # Calculate values according to type ID
        if type_id == 0:
            number = sum(subpackets)
        elif type_id == 1:
            number = reduce((lambda x, y: x * y), subpackets)
        elif type_id == 2:
            number = min(subpackets)
        elif type_id == 3:
            number = max(subpackets)
        elif type_id == 5:
            number = int(subpackets[0] > subpackets[1])
        elif type_id == 6:
            number = int(subpackets[0] < subpackets[1])
        elif type_id == 7:
            number = int(subpackets[0] == subpackets[1])
        else:
            raise ValueError

        return number, bits, packet_version


def main():
    input_file = read_input("2021/16/input.txt")[0]
    encoded = "".join([bin(int(char, 16))[2:].zfill(4) for char in input_file])
    number, _, version_sum = _decode(encoded)
    print(f"Result of part 1: {version_sum}")
    print(f"Result of part 2: {number}")


if __name__ == "__main__":
    main()
