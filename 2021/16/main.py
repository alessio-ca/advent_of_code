from utils import read_input
from typing import Tuple, List
from functools import reduce


def _extract_literal(bits: str) -> Tuple[int, str]:
    """Extract number as literal. Used when type ID is literal"""
    # Take substrings
    repr = ""
    # Loop until the prefix to the group is '1' (last group)
    while bits[0] != "0":
        repr, bits = repr + bits[1:5], bits[5:]
    repr, bits = repr + bits[1:5], bits[5:]
    # Return the number representation in decimal
    number = int(repr, 2)
    return number, bits


def _extract_operator(bits: str) -> Tuple[List[int], str, int]:
    """Extract list of subpacket numbers. Used when if type ID is operator"""
    len_type_id, bits = bits[0], bits[1:]
    subpackets = []
    packet_version = 0

    if int(len_type_id):
        # Next 11 bits specify the number of subpackets
        n_subpackets, bits = int(bits[:11], 2), bits[11:]
        for _ in range(n_subpackets):
            # Treat subpackets by recursively decoding them
            subpacket_number, bits, sub_packet_version = decode(bits)
            packet_version += sub_packet_version
            subpackets.append(subpacket_number)
    else:
        # Next 15 bits specify the length of subpackets
        len_subpackets, bits = int(bits[:15], 2), bits[15:]
        first_size = len(bits)
        while (first_size - len(bits)) < len_subpackets:
            # Treat subpackets by recursively decoding them
            subpacket, bits, sub_packet_version = decode(bits)
            packet_version += sub_packet_version
            subpackets.append(subpacket)

    return subpackets, bits, packet_version


def _calculate_number(type_id: int, subpackets: List[int]) -> int:
    """Calculate number from list of subpacket numbers according to type ID"""
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

    return number


def decode(string: str) -> Tuple[int, str, int]:
    """General function to decode a string"""
    packet_version, type_id, bits = int(string[:3], 2), int(string[3:6], 2), string[6:]

    if type_id == 4:
        # This is a literal
        number, bits = _extract_literal(bits)
        return number, bits, packet_version

    else:
        # This is an operator
        subpackets, bits, subpacket_version = _extract_operator(bits)
        packet_version += subpacket_version
        number = _calculate_number(type_id, subpackets)
        return number, bits, packet_version


def main():
    input_file = read_input("2021/16/input.txt")[0]
    encoded = "".join([bin(int(char, 16))[2:].zfill(4) for char in input_file])
    number, _, version_sum = decode(encoded)
    print(f"Result of part 1: {version_sum}")
    print(f"Result of part 2: {number}")


if __name__ == "__main__":
    main()
