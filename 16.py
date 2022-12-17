GIVEN_FILE_NAME = "given_16.txt"
INPUT_FILE_NAME = "input_16.txt"

from typing import Tuple


class Cave:
    def __init__(self, column_number: int, row_number: int):
        self.rows: list[list] = [["."] * column_number for _ in range(row_number)]

    def add_row(self, row: list):
        self.rows.append(row)

    def get_rows(self) -> "list[list]":
        return self.rows

    def get_columns(self) -> "list[list]":
        return list(map(list, zip(*self.rows)))

    def get_item(self, column, row):
        return self.rows[row][column]

    def set_item(self, column, row, item):
        self.rows[row][column] = item

    def fill_rock(self, path: "list[Tuple[int, int]]"):
        last_column, last_row = path[0]
        for point in path[1:]:
            current_column, current_row = point
            if last_column == current_column:
                # fill Y
                diff = abs(current_row - last_row)
                for i in range(diff + 1):
                    self.set_item(current_column, min(current_row, last_row) + i, "#")
            elif last_row == current_row:
                # fill X
                diff = abs(current_column - last_column)
                for i in range(diff + 1):
                    self.set_item(
                        min(current_column, last_column) + i, current_row, "#"
                    )
            last_column, last_row = current_column, current_row

    def get_minimum_row_for_each_column(self) -> dict:
        minimum_row_dict: dict = dict()
        for i, column in enumerate(self.get_columns()):
            minimum_row = None
            for j, row in enumerate(column):
                if row == "#":
                    minimum_row = j
            minimum_row_dict[i] = minimum_row
        return minimum_row_dict

    def add_bottom(self):
        minimum_row: int = None
        for column in self.get_columns():
            for j, row in enumerate(column):
                if row == "#":
                    if not minimum_row or j > minimum_row:
                        minimum_row = j
        for column in range(len(self.rows[0])):
            self.set_item(column, minimum_row + 2, "#")

    def simulate_single_sand_fall(self, minimum_row_dict: dict) -> bool:
        sand_column, sand_row = (500, 0)
        if self.get_item(sand_column, sand_row) != ".":
            return False
        while (
            minimum_row_dict[sand_column] and sand_row < minimum_row_dict[sand_column]
        ):
            # check below
            below = self.get_item(sand_column, sand_row + 1)
            diagonally_left = self.get_item(sand_column - 1, sand_row + 1)
            diagonally_right = self.get_item(sand_column + 1, sand_row + 1)
            if below == ".":
                sand_row += 1
            elif diagonally_left == ".":
                sand_column -= 1
                sand_row += 1
            elif diagonally_right == ".":
                sand_column += 1
                sand_row += 1
            else:
                self.set_item(sand_column, sand_row, "O")
                return True
        return False

    def simulate_sand_fall(self) -> int:
        minimum_row_dict = self.get_minimum_row_for_each_column()
        total_count = 0
        while self.simulate_single_sand_fall(minimum_row_dict):
            total_count += 1
        return total_count

    def __repr__(self):
        return "\n".join("".join(str(item) for item in row) for row in self.rows)


class Solver:
    def parse_file(self, input_file_name: str) -> Cave:
        cave = Cave(1000, 1000)
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                point_raw_list = stripped_line.split(" -> ")
                path: "list[Tuple[int, int]]" = []
                for point_raw in point_raw_list:
                    path.append(tuple(int(point) for point in point_raw.split(",")))
                cave.fill_rock(path)
        return cave


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        cave: Cave = solver.parse_file(input_file_name)
        number_of_sand_falls = cave.simulate_sand_fall()
        return number_of_sand_falls

    def test_given_1(self):
        number_of_sand_falls = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(number_of_sand_falls, 24)

    def test_input_1(self):
        number_of_sand_falls = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(number_of_sand_falls, 1199)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        cave: Cave = solver.parse_file(input_file_name)
        cave.add_bottom()
        number_of_sand_falls = cave.simulate_sand_fall()
        return number_of_sand_falls

    def test_given_2(self):
        number_of_sand_falls = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(number_of_sand_falls, 93)

    def test_input_2(self):
        number_of_sand_falls = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(number_of_sand_falls, 23925)


unittest.main(exit=False)
