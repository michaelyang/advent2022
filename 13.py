GIVEN_FILE_NAME = "given_13.txt"
INPUT_FILE_NAME = "input_13.txt"

from typing import Tuple
import ast
from functools import cmp_to_key


class Packet:
    def __init__(self, raw_packet: str) -> None:
        self.value = ast.literal_eval(raw_packet)

    @staticmethod
    def is_greater_than(current_item, other_item):
        if isinstance(current_item, list) and isinstance(other_item, list):
            if len(current_item) == 0 and len(other_item) == 0:
                return False
            if len(current_item) == 0 and len(other_item) != 0:
                return False
            if len(other_item) == 0 and len(current_item) != 0:
                return True
            number_of_items_to_comapre = min(len(current_item), len(other_item))
            for i in range(number_of_items_to_comapre):
                if Packet.is_greater_than(current_item[i], other_item[i]):
                    return True
            # Same length
            if len(current_item) == len(other_item):
                return False
            # left side ran out of items, inputs are in correct order as long as last one is less than or equal to
            if len(current_item) < len(other_item):
                if Packet.is_less_than_or_equal_to(
                    current_item[number_of_items_to_comapre - 1],
                    other_item[number_of_items_to_comapre - 1],
                ):
                    return False
                else:
                    return True
            # rightside ran out side ran out of items
            else:
                return True
        elif isinstance(current_item, list):
            return Packet.is_greater_than(current_item, [other_item])
        elif isinstance(other_item, list):
            return Packet.is_greater_than([current_item], other_item)
        elif current_item > other_item:
            return True

    @staticmethod
    def is_less_than(current_item, other_item):
        # print("Comparing {} and {}".format(current_item, other_item))
        if isinstance(current_item, list) and isinstance(other_item, list):
            if len(current_item) == 0 and len(other_item) == 0:
                return False
            if len(current_item) == 0 and len(other_item) != 0:
                # print("EMPTY")
                return True
            if len(other_item) == 0 and len(current_item) != 0:
                return False
            number_of_items_to_comapre = min(len(current_item), len(other_item))
            # print("Comparing {} elements".format(number_of_items_to_comapre))
            for i in range(number_of_items_to_comapre):
                if Packet.is_less_than(current_item[i], other_item[i]):
                    """
                    print(
                        "{} is less than {}".format(
                            current_item[i],
                            other_item[i],
                        )
                    )
                    """
                    return True
                if Packet.is_greater_than(current_item[i], other_item[i]):
                    """
                    print(
                        "{} is less than {}".format(
                            current_item[i],
                            other_item[i],
                        )
                    )
                    """
                    return False
            # Same
            if len(current_item) == len(other_item):
                return False
            # left side ran out of items, inputs are in correct order as long as last one is less than or equal to
            if len(current_item) < len(other_item):
                return True
            else:
                return False
        elif isinstance(current_item, list):
            return Packet.is_less_than(current_item, [other_item])
        elif isinstance(other_item, list):
            return Packet.is_less_than([current_item], other_item)
        elif current_item < other_item:
            # print("{} is less than {}".format(current_item, other_item))
            return True

    def __repr__(self):
        return str(self.value)


class Solver:
    def parse_file(self, input_file_name: str) -> "list[Tuple(Packet, Packet)]":
        list_of_packet_pairs: list[Tuple(Packet, Packet)] = []
        with open(input_file_name) as f:
            packet_pairs: list[Packet] = []
            for line in f:
                if line in ["\n", "\r\n"]:
                    continue
                stripped_line: str = line.strip()
                if not packet_pairs:
                    packet_pairs.append(Packet(stripped_line))
                else:
                    packet_pairs.append(Packet(stripped_line))
                    list_of_packet_pairs.append(tuple(packet_pairs))
                    packet_pairs = []
        return list_of_packet_pairs

    def parse_file_2(self, input_file_name: str) -> "list[Packet]":
        list_of_packets: list[Packet] = []
        with open(input_file_name) as f:
            for line in f:
                if line in ["\n", "\r\n"]:
                    continue
                stripped_line: str = line.strip()
                list_of_packets.append(Packet(stripped_line))
        return list_of_packets


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_packet_pairs = solver.parse_file(input_file_name)
        sum_of_right_order_indicies = 0
        for i in range(len(list_of_packet_pairs)):
            packet_1, packet_2 = list_of_packet_pairs[i]
            if Packet.is_less_than(packet_1.value, packet_2.value):
                sum_of_right_order_indicies += i + 1
        return sum_of_right_order_indicies

    def test_given_1(self):
        sum_of_right_order_indicies = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(sum_of_right_order_indicies, 13)

    def test_input_1(self):
        sum_of_right_order_indicies = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(sum_of_right_order_indicies, 5682)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_packets = solver.parse_file_2(input_file_name)
        list_of_packets.append(Packet("[[2]]"))
        list_of_packets.append(Packet("[[6]]"))
        product_of_decoder_key = 1
        list_of_packets.sort(
            key=cmp_to_key(
                lambda x, y: -1 if Packet.is_less_than(x.value, y.value) else 1
            )
        )
        for i in range(len(list_of_packets)):
            packet = list_of_packets[i]
            if packet.value == [[2]] or packet.value == [[6]]:
                product_of_decoder_key *= i + 1
        return product_of_decoder_key

    def test_given_2(self):
        product_of_decoder_key = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(product_of_decoder_key, 140)

    def test_input_2(self):
        product_of_decoder_key = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(product_of_decoder_key, 20304)


unittest.main(exit=False)
