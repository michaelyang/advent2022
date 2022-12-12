GIVEN_FILE_NAME = "given_11.txt"
INPUT_FILE_NAME = "input_11.txt"

from typing import Callable
import math


class Monkey:
    def __init__(
        self,
        name: str,
        starting_items: "list[int]",
        operatrion: Callable[[int], int],
        test_divisor: int,
        true_monkey: str,
        false_monkey: str,
    ) -> None:
        self.name = name
        self.items = starting_items
        self.operation: Callable[[int], int] = operatrion
        self.test_divisor: int = test_divisor
        self.true_monkey: str = true_monkey
        self.false_monkey: str = false_monkey
        self.number_of_inspected_items: int = 0

    def add_item(self, item: int) -> None:
        self.items.append(item)

    def inspect_items(self) -> None:
        self.number_of_inspected_items += len(self.items)
        self.items = [self.operation(item) for item in self.items]

    def get_bored(self, divide_by_three: bool = True, safe_divisor: int = None) -> None:
        if divide_by_three:
            self.items = [(item // 3) for item in self.items]
        else:
            self.items = [(item % safe_divisor) for item in self.items]

    def get_item(self) -> int:
        if len(self.items) > 0:
            return self.items.pop(0)
        return None

    def __repr__(self) -> str:
        return "Monkey {}: {}".format(self.name, ", ".join(map(str, self.items)))


class Solver:
    NUMBER_OF_LINES_FOR_MONKEY_DATA = 6

    def parse_file(self, input_file_name: str) -> "list[Monkey]":
        list_of_monkeys: list[Monkey] = []
        with open(input_file_name) as f:
            monkey_data_raw = []
            for line in f:
                if line.strip():
                    monkey_data_raw.append(line.strip())
                if len(monkey_data_raw) >= self.NUMBER_OF_LINES_FOR_MONKEY_DATA:
                    monkey_name_raw: str = (
                        monkey_data_raw[0].strip().split()[1].replace(":", "")
                    )
                    starting_items_raw: list[str] = (
                        monkey_data_raw[1]
                        .replace("Starting items:", "")
                        .strip()
                        .split(", ")
                    )
                    operation_raw: str = (
                        monkey_data_raw[2].replace("Operation:", "").strip()
                    )
                    test_divisor_raw: str = (
                        monkey_data_raw[3].replace("Test: divisible by", "").strip()
                    )
                    true_monkey_raw: str = (
                        monkey_data_raw[4]
                        .replace("If true: throw to monkey", "")
                        .strip()
                    )
                    false_monkey_raw: str = (
                        monkey_data_raw[5]
                        .replace("If false: throw to monkey", "")
                        .strip()
                    )
                    monkey: Monkey = Monkey(
                        monkey_name_raw,
                        [int(item) for item in starting_items_raw],
                        self.parse_operation(operation_raw),
                        int(test_divisor_raw),
                        true_monkey_raw,
                        false_monkey_raw,
                    )
                    list_of_monkeys.append(monkey)
                    monkey_data_raw = []
        return list_of_monkeys

    def parse_operation(self, operation_raw: str) -> Callable[[int], int]:
        stripped_operation: str = operation_raw.replace("new = ", "")
        left_raw, operator, right_raw = stripped_operation.split()
        left = "x" if left_raw == "old" else left_raw
        right = "x" if right_raw == "old" else right_raw
        function_raw = " ".join([left, operator, right])
        return lambda x: eval(function_raw)

    def play_one_round(
        self, list_of_monkeys: "list[Monkey]", divide_by_three=True
    ) -> None:
        safe_divisor = math.prod(monkey.test_divisor for monkey in list_of_monkeys)
        for monkey in list_of_monkeys:
            monkey.inspect_items()
            monkey.get_bored(divide_by_three, safe_divisor)
            item = monkey.get_item()
            while item:
                if item % monkey.test_divisor == 0:
                    list_of_monkeys[int(monkey.true_monkey)].add_item(item)
                else:
                    list_of_monkeys[int(monkey.false_monkey)].add_item(item)

                item = monkey.get_item()


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_monkeys: list[Monkey] = solver.parse_file(input_file_name)
        for _ in range(20):
            solver.play_one_round(list_of_monkeys)
        sorted_number_of_inspected_items = sorted(
            [monkey.number_of_inspected_items for monkey in list_of_monkeys]
        )
        return (
            sorted_number_of_inspected_items[-1] * sorted_number_of_inspected_items[-2]
        )

    def test_given_1(self):
        monkey_business = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(monkey_business, 10605)
        return

    def test_input_1(self):
        monkey_business = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(monkey_business, 102399)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_monkeys: list[Monkey] = solver.parse_file(input_file_name)
        for _ in range(10000):
            solver.play_one_round(list_of_monkeys, False)
        sorted_number_of_inspected_items = sorted(
            [monkey.number_of_inspected_items for monkey in list_of_monkeys]
        )
        return (
            sorted_number_of_inspected_items[-1] * sorted_number_of_inspected_items[-2]
        )

    def test_given_2(self):
        monkey_business = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(monkey_business, 2713310158)

    def test_input_2(self):
        monkey_business = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(monkey_business, 23641658401)


unittest.main(exit=False)
