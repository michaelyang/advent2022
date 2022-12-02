INPUT_FILE_NAME = "input_1.txt"


class Food:
    def __init__(self, calories: int) -> None:
        self.calories = calories

    def get_calories(self) -> int:
        return self.calories


class Elf:
    def __init__(self) -> None:
        self.foods = []

    def add_food(self, food: Food) -> None:
        self.foods.append(food)

    def get_total_food_calories(self):
        return sum(food.get_calories() for food in self.foods)


class Solver:
    EMPTY_LINE = "\n"

    def parse_file(self, input_file_name: str) -> "list[Elf]":
        list_of_elves: list[Elf] = []
        with open(input_file_name) as f:
            current_elf = None
            for line in f:
                if line == self.EMPTY_LINE and current_elf:
                    list_of_elves.append(current_elf)
                    current_elf = None
                else:
                    if not current_elf:
                        current_elf = Elf()
                    food = Food(int(line.strip()))
                    current_elf.add_food(food)
        return list_of_elves

    def sort_elves_by_food_calories(self, list_of_elves):
        return sorted(list_of_elves, key=lambda elf: elf.get_total_food_calories())


import unittest


class SolverTest(unittest.TestCase):
    def test_1(self):
        solver = Solver()
        list_of_elves = solver.parse_file(INPUT_FILE_NAME)
        sorted_list_of_elves: list[Elf] = solver.sort_elves_by_food_calories(
            list_of_elves
        )
        self.assertEqual(sorted_list_of_elves[-1].get_total_food_calories(), 69289)

    def test_2(self):
        solver = Solver()
        list_of_elves = solver.parse_file(INPUT_FILE_NAME)
        sorted_list_of_elves: list[Elf] = solver.sort_elves_by_food_calories(
            list_of_elves
        )
        self.assertEqual(
            sum(elf.get_total_food_calories() for elf in sorted_list_of_elves[-3:]),
            205615,
        )


unittest.main(exit=False)
