GIVEN_FILE_NAME = "given_3.txt"
INPUT_FILE_NAME = "input_3.txt"
from typing import Optional


class Item:
    def __init__(self, value: str) -> None:
        self.value = value

    def get_priority(self) -> int:
        if ord(self.value) >= ord("A") and ord(self.value) <= ord("Z"):
            return ord(self.value) - ord("A") + 27
        else:
            return ord(self.value) - ord("a") + 1

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Item):
            return False
        return self.value == __o.value

    def __hash__(self):
        return hash(self.value)


class Rucksack:
    def __init__(self, items: "list[Item]") -> None:
        self.all_items = [Item(value) for value in items]
        self.large_compartment_1 = [Item(value) for value in items[: len(items) // 2]]
        self.large_compartment_2 = [Item(value) for value in items[len(items) // 2 :]]

    def get_overlapping_items(self) -> "list[Item]":
        large_compartment_1_set: set[Item] = set(self.large_compartment_1)
        return list(
            set(
                filter(
                    lambda item: item in large_compartment_1_set,
                    self.large_compartment_2,
                )
            )
        )

    def get_sum_of_priorities_of_overlapping_items(self):
        overlapping_items: list[Item] = self.get_overlapping_items()
        return sum(item.get_priority() for item in overlapping_items)


class Group:
    def __init__(self, rucksacks: "list[Rucksack]") -> None:
        self.rucksacks: list[Rucksack] = rucksacks

    def get_badge(self) -> Optional[Item]:
        if len(self.rucksacks) < 2:
            return None
        union_set: set(Item) = set(self.rucksacks[0].all_items)
        for rucksack in self.rucksacks[1:]:
            union_set = union_set & set(rucksack.all_items)
        # Hacky, only return one item
        return list(union_set)[0]


class Solver:
    def parse_file(self, input_file_name: str) -> "list[Rucksack]":
        list_of_rucksacks: list[Rucksack] = []
        with open(input_file_name) as f:
            for line in f:
                rucksack = Rucksack(line.strip())
                list_of_rucksacks.append(rucksack)
        return list_of_rucksacks

    def get_total_priorities(self, list_of_rucksacks: "list[Rucksack]") -> int:
        return sum(
            rucksack.get_sum_of_priorities_of_overlapping_items()
            for rucksack in list_of_rucksacks
        )

    def get_total_badge_priorities(self, list_of_rucksacks: "list[Rucksack]") -> int:
        GROUP_SIZE = 3
        total_badge_prioirites: int = 0
        for group_rucksacks in zip(*[iter(list_of_rucksacks)] * GROUP_SIZE):
            group = Group(group_rucksacks)
            badge = group.get_badge()
            total_badge_prioirites += badge.get_priority()
        return total_badge_prioirites


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_rucksacks: list[Rucksack] = solver.parse_file(input_file_name)
        return solver.get_total_priorities(list_of_rucksacks)

    def test_given_1(self):
        total_priorities = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(total_priorities, 157)

    def test_input_1(self):
        total_priorities = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(total_priorities, 8252)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_rucksacks: list[Rucksack] = solver.parse_file(input_file_name)
        return solver.get_total_badge_priorities(list_of_rucksacks)

    def test_given_2(self):
        total_priorities = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(total_priorities, 70)

    def test_input_2(self):
        total_priorities = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(total_priorities, 2828)


unittest.main(exit=False)
