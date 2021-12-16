"""
Advent of Code - tentative pour J16.

Daniel Kessler (aka Dalker), le 2021.12.16
"""

import operator
from functools import reduce
from math import prod
from collections import deque

DAY = "16"
HINTS = ("D2FE28", "38006F45291200", "EE00D40C823060", "8A004A801A8002F478",
         "620080001611562C8802118E34", "C0015000016115A2E0802F182340",
         "A0016C880162017C3686B18A3D4780")
HINTS2 = ("C200B40A82", "04005AC33890", "880086C3E88112", "CE00C43D881120",
          "D8005AC2A8F0", "F600BC2D8F", "9C005AC2F8F0",
          "9C0141080250320F1802104A08")


def get_data(fname: str) -> str:
    """Read the day's input and return contents in adequate data structure."""
    with open(f"{fname}.txt") as datafile:
        data = datafile.readline().strip()
    return data


class BitStream:
    """A stream of bits produced by a hex string."""

    def __init__(self, transmission: str):
        self.hex_buffer = deque(transmission)
        self.bits = self._get_bit()
        self.count = 0

    def _get_bit(self):
        """Generate one bits one at a time from transmission."""
        while self.hex_buffer:
            half_octet = "{:0>4s}".format(bin(int(self.hex_buffer.popleft(),
                                                  16))[2:])
            for bit in half_octet:
                yield bit

    def get(self, n_bits: int) -> str:
        """Read some bits.

        Return the requested amount of bits, as a str of 0s and 1s.
        """
        read = "".join(next(self.bits) for _ in range(n_bits))
        self.count += n_bits
        return read


class Packet:
    """A Buoyancy Interchange Transmission System packet."""
    OPNAMES = ["sum", "product", "min", "max", "literal", "greater than",
               "less than", "equal"]
    OPFUNCS = [sum, prod, min, max, None,
               lambda v: reduce(operator.__gt__, v),
               lambda v: 1 if v[0] < v[1] else 0,
               lambda v: 1 if v[0] == v[1] else 0]

    def __init__(self, bits: BitStream, level=0):
        self.bits = bits
        self.level = level
        self.version = int(self.bits.get(3), 2)
        self.typeid = int(self.bits.get(3), 2)
        self.op = self.OPNAMES[self.typeid]
        self._subpackets = []
        if self.op == "literal":
            self.value = self._read_number()
        else:
            self._read_subpackets()
            self.evaluate()

    def evaluate(self):
        """Perform this packet's operation."""
        values = [packet.value for packet in self._subpackets]
        self.value = self.OPFUNCS[self.typeid](values)

    def total_versions(self):
        """Return sum of versions."""
        total = self.version
        for packet in self._subpackets:
            total += packet.total_versions()
        return total

    def __repr__(self):
        res = " "*self.level
        res += f"Packet(v{self.version}, t{self.typeid}, "
        res += f"op: {self.op}, value: {self.value})"
        for subpacket in self._subpackets:
            res += "\n" + repr(subpacket)
        return res

    def _read_number(self):
        """Read a number from remaining bits."""
        number = ""
        cont = "1"
        while cont == "1":
            cont = self.bits.get(1)
            number += self.bits.get(4)
        return int(number, 2)

    def _read_subpackets(self):
        """Read subpackets from current packet."""
        length_type_id = self.bits.get(1)
        if length_type_id == "0":
            length = int(self.bits.get(15), 2)
            init_count = self.bits.count
            while self.bits.count < init_count + length:
                self._subpackets.append(Packet(self.bits, self.level+1))
        else:
            number = int(self.bits.get(11), 2)
            for _ in range(number):
                self._subpackets.append(Packet(self.bits, self.level+1))


def decode(message: str) -> Packet:
    """Decode a BITS message."""
    stream = BitStream(message)
    message = Packet(stream)
    return message


if __name__ == "__main__":
    realdata = get_data(f"input{DAY}")
    realmessage = decode(realdata)
    for n_hint, hint in enumerate(HINTS):
        print(f"* hint {n_hint + 1} : {hint} *")
        message = decode(hint)
        # print(message)
        print("--> Total Versions:", message.total_versions())
    print("part 1:", realmessage.total_versions())
    for n_hint, hint in enumerate(HINTS2):
        print(f"* hint {n_hint + 1} : {hint} *")
        message = decode(hint)
        print(message)
    print("part 2:", realmessage.value)
