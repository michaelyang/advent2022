GIVEN_FILE_NAME = "given_10.txt"
INPUT_FILE_NAME = "input_10.txt"

from enum import Enum
from typing import Tuple


class Operation:
    def __init__(self, number_of_cycles: int) -> None:
        self.number_of_cycles = number_of_cycles


class NoOperation(Operation):
    NUMBER_OF_CYCLES = 1

    def __init__(self) -> None:
        super().__init__(self.NUMBER_OF_CYCLES)


class AddOperation(Operation):
    NUMBER_OF_CYCLES = 2

    def __init__(self, to_add: int) -> None:
        super().__init__(self.NUMBER_OF_CYCLES)
        self.to_add = to_add


class Program:
    def __init__(self) -> None:
        self.cycle: int = 0
        self.x: int = 1

    # returns of a tuple of cycle and x
    def apply_operation(self, operation: Operation) -> "list[Tuple(int, int)]":
        result: list[Tuple(int, int)] = []
        for i in range(operation.number_of_cycles):
            self.cycle += 1
            if isinstance(operation, AddOperation) and i == (
                operation.number_of_cycles - 1
            ):
                self.x += operation.to_add
            result.append((self.cycle, self.x))
        return result

    # returns of a tuple of cycle and x
    def apply_operations(
        self, list_of_operations: "list[Operation]"
    ) -> "list[Tuple(int, int)]":
        result: list[Tuple(int, int)] = []
        for operation in list_of_operations:
            single_result = self.apply_operation(operation)
            result.extend(single_result)
        return result

    def __repr__(self) -> str:
        return "- {} (file, size={})".format(self.name, self.size)


class Solver:
    NO_OPERATION = "noop"
    ADD_OPERATION = "addx"

    def parse_file(self, input_file_name: str) -> "list[Operation]":
        list_of_operations: list[Operation] = []
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                split_line = stripped_line.split()
                if split_line[0] == self.NO_OPERATION:
                    list_of_operations.append(NoOperation())
                elif split_line[0] == self.ADD_OPERATION:
                    list_of_operations.append(AddOperation(int(split_line[1])))
        return list_of_operations


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_operations: list[Operation] = solver.parse_file(input_file_name)
        program = Program()
        list_of_results = program.apply_operations(list_of_operations)
        sum_of_signal_strengths: int = 0
        if len(list_of_results) < 20:
            return sum_of_signal_strengths
        for i in range(18, len(list_of_results), 40):
            cycle, x = list_of_results[i]
            sum_of_signal_strengths += x * (cycle + 1)
        return sum_of_signal_strengths

    def test_given_1(self):
        sum_of_signal_strengths = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(sum_of_signal_strengths, 13140)

    def test_input_1(self):
        sum_of_signal_strengths = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(sum_of_signal_strengths, 16880)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_operations: list[Operation] = solver.parse_file(input_file_name)
        program = Program()
        list_of_results = program.apply_operations(list_of_operations)
        display: list[str] = []
        current_str = []
        prev_x = 1
        for i in range(len(list_of_results)):
            horizontal_position = i % 40
            cycle, x = list_of_results[i]
            if prev_x - 1 <= horizontal_position and horizontal_position <= prev_x + 1:
                current_str.append("#")
            else:
                current_str.append(".")
            prev_x = x
            if cycle % 40 == 0:
                display.append("".join(current_str))
                current_str = []
        return "\n".join(display)

    def test_input_2(self):
        display = self.solve_2(GIVEN_FILE_NAME)
        print("\n")
        print(display)
        self.assertEqual(
            display,
            """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....""",
        )

    def test_input_2(self):
        display = self.solve_2(INPUT_FILE_NAME)
        print("\n")
        print(display)
        self.assertEqual(
            display,
            """###..#..#..##..####..##....##.###..###..
#..#.#.#..#..#....#.#..#....#.#..#.#..#.
#..#.##...#..#...#..#..#....#.###..#..#.
###..#.#..####..#...####....#.#..#.###..
#.#..#.#..#..#.#....#..#.#..#.#..#.#.#..
#..#.#..#.#..#.####.#..#..##..###..#..#.""",
        )


unittest.main(exit=False)
