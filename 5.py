GIVEN_FILE_NAME = "given_5.txt"
INPUT_FILE_NAME = "input_5.txt"

from typing import Tuple


class Move:
    def __init__(self, number: int, from_stack: int, to_stack: int) -> None:
        self.number = number
        self.from_stack = from_stack
        self.to_stack = to_stack

    def __repr__(self) -> str:
        return "move {} from {} to {}".format(
            self.number, self.from_stack, self.to_stack
        )


class Stack:
    def __init__(self, items=None) -> None:
        self.items = items if items is not None else []

    def add_item(self, item) -> None:
        self.items.append(item)

    def get_top_item(self):
        if not self.items:
            return None
        top_item = self.items.pop()
        return top_item

    def get_top_n_items(self, n: int):
        if not self.items:
            return None
        number_of_items = min(n, len(self.items))
        top_items = self.items[len(self.items) - number_of_items :]
        self.items = self.items[: len(self.items) - number_of_items]
        return top_items

    def add_stack_of_items(self, items):
        self.items.extend(items)

    def peak_top_item(self):
        if not self.items:
            return None
        return self.items[-1]

    def __repr__(self) -> str:
        return str(self.items)


class Solver:
    CRATE_START = "["
    CRATE_END = "]"

    def parse_file(self, input_file_name: str) -> Tuple["list[Stack]", "list[Move]"]:
        list_of_raw_rows: list[str] = []
        list_of_stacks: list[Stack] = []
        list_of_moves: list[Move] = []
        with open(input_file_name) as f:
            is_stack_data: bool = True
            for line in f:
                if line in ["\n", "\r\n"]:
                    # end of stack data, build stacks
                    number_of_stacks = len(list_of_raw_rows[-1]) // 4
                    list_of_stacks = [Stack() for _ in range(number_of_stacks)]
                    for raw_row in list_of_raw_rows[-2::-1]:
                        current_column: int = 0
                        while current_column < len(raw_row) // 4:
                            start_index = (current_column) * 4
                            crate: str = raw_row[start_index : start_index + 3]
                            crate_letter = (
                                crate.replace(self.CRATE_START, "")
                                .replace(self.CRATE_END, "")
                                .strip()
                            )
                            if crate_letter:
                                list_of_stacks[current_column].add_item(crate_letter)
                            current_column += 1
                    is_stack_data = False
                elif is_stack_data:
                    list_of_raw_rows.append(line)
                else:
                    number, from_stack, to_stack = [
                        int(s) for s in line.split() if s.isdigit()
                    ]
                    move = Move(number, from_stack, to_stack)
                    list_of_moves.append(move)
        return list_of_stacks, list_of_moves

    def perform_moves_1(
        self, list_of_stacks: "list[Stack]", list_of_moves: "list[Move]"
    ) -> None:
        for move in list_of_moves:
            for _ in range(move.number):
                item = list_of_stacks[move.from_stack - 1].get_top_item()
                list_of_stacks[move.to_stack - 1].add_item(item)

    def perform_moves_2(
        self, list_of_stacks: "list[Stack]", list_of_moves: "list[Move]"
    ) -> None:
        for move in list_of_moves:
            items = list_of_stacks[move.from_stack - 1].get_top_n_items(move.number)
            list_of_stacks[move.to_stack - 1].add_stack_of_items(items)


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_stacks, list_of_moves = solver.parse_file(input_file_name)
        solver.perform_moves_1(list_of_stacks, list_of_moves)
        list_of_top_items = []
        for stack in list_of_stacks:
            list_of_top_items.append(stack.peak_top_item())
        return "".join(list_of_top_items)

    def test_given_1(self):
        string_of_top_items = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(string_of_top_items, "CMZ")

    def test_input_1(self):
        string_of_top_items = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(string_of_top_items, "MQSHJMWNH")

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_stacks, list_of_moves = solver.parse_file(input_file_name)
        solver.perform_moves_2(list_of_stacks, list_of_moves)
        list_of_top_items = []
        for stack in list_of_stacks:
            list_of_top_items.append(stack.peak_top_item())
        return "".join(list_of_top_items)

    def test_given_2(self):
        string_of_top_items = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(string_of_top_items, "MCD")

    def test_input_2(self):
        string_of_top_items = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(string_of_top_items, "LLWJRBHVZ")


unittest.main(exit=False)
