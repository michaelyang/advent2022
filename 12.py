GIVEN_FILE_NAME = "given_12.txt"
INPUT_FILE_NAME = "input_12.txt"

from typing import List, Tuple


class Grid:
    def __init__(self):
        self.rows: List[list] = []
        self.starting_point: Tuple(int, int) = None
        self.ending_point: Tuple(int, int) = None

    def add_row(self, row: list):
        self.rows.append(row)

    def get_rows(self) -> List[list]:
        return self.rows

    def get_columns(self) -> List[list]:
        return list(map(list, zip(*self.rows)))

    def get_item(self, column, row):
        if (
            row < 0
            or column < 0
            or row >= len(self.rows)
            or column >= len(self.rows[0])
        ):
            return None
        return self.rows[row][column]

    def set_starting_point(self, column: int, row: int):
        self.starting_point = (column, row)

    def set_ending_point(self, column: int, row: int):
        self.ending_point = (column, row)

    def __repr__(self):
        return "\n".join("".join(str(item) for item in row) for row in self.rows)


class Solver:
    STARTING_POINT = "S"
    ENDING_POINT = "E"

    def parse_file(self, input_file_name: str) -> Grid:
        grid = Grid()
        current_row = 0
        with open(input_file_name) as f:
            current_column = 0
            for line in f:
                stripped_line: str = line.strip()
                list_of_elevations: list[str] = []
                for elevation_raw in stripped_line:
                    if elevation_raw == self.STARTING_POINT:
                        list_of_elevations.append("a")
                        grid.set_starting_point(current_column, current_row)
                    elif elevation_raw == self.ENDING_POINT:
                        list_of_elevations.append("z")
                        grid.set_ending_point(current_column, current_row)
                    else:
                        list_of_elevations.append(elevation_raw)
                    current_column += 1
                grid.add_row(list_of_elevations)
                current_column = 0
                current_row += 1
        return grid

    def get_shortest_scenic_path(self, grid: Grid) -> int:
        min_length = None
        current_row = 0
        possible_starting_points = []
        for row in grid.rows:
            current_column = 0
            for height in row:
                if height == "a" or height == "S":
                    possible_starting_points.append((current_column, current_row))
                current_column += 1
            current_row += 1
        for starting_point in possible_starting_points:
            column, row = starting_point
            grid.set_starting_point(column, row)
            length = self.get_shortest_path_length(grid)
            if length > 0 and (min_length is None or length < min_length):
                min_length = length
        return min_length

    def get_shortest_path_length(self, grid: Grid) -> int:
        starting_column, starting_row = grid.starting_point
        ending_column, ending_row = grid.ending_point
        points_to_visit = [(starting_column, starting_row, 0)]
        min_length = None
        visited_points = set()
        while points_to_visit:
            current_column, current_row, length_so_far = points_to_visit.pop(0)
            if current_column == ending_column and current_row == ending_row:
                if min_length is None or length_so_far < min_length:
                    min_length = length_so_far
            current_elevation = grid.get_item(current_column, current_row)
            # Top
            top_elevation = grid.get_item(current_column, current_row - 1)
            if (
                top_elevation
                and ord(top_elevation) <= (ord(current_elevation) + 1)
                and (current_column, current_row - 1) not in visited_points
            ):
                points_to_visit.append(
                    (current_column, current_row - 1, length_so_far + 1)
                )
                visited_points.add((current_column, current_row - 1))

            # Left
            left_elevation = grid.get_item(current_column - 1, current_row)
            if (
                left_elevation
                and ord(left_elevation) <= (ord(current_elevation) + 1)
                and (current_column - 1, current_row) not in visited_points
            ):
                points_to_visit.append(
                    (current_column - 1, current_row, length_so_far + 1)
                )
                visited_points.add((current_column - 1, current_row))

            # Bottom
            bottom_elevation = grid.get_item(current_column, current_row + 1)
            if (
                bottom_elevation
                and ord(bottom_elevation) <= (ord(current_elevation) + 1)
                and (current_column, current_row + 1) not in visited_points
            ):
                points_to_visit.append(
                    (current_column, current_row + 1, length_so_far + 1)
                )
                visited_points.add((current_column, current_row + 1))

            # Right
            right_elevation = grid.get_item(current_column + 1, current_row)
            if (
                right_elevation
                and ord(right_elevation) <= (ord(current_elevation) + 1)
                and (current_column + 1, current_row) not in visited_points
            ):
                points_to_visit.append(
                    (current_column + 1, current_row, length_so_far + 1)
                )
                visited_points.add((current_column + 1, current_row))
        return min_length or -1


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        grid = solver.parse_file(input_file_name)
        shortest_path_length: int = solver.get_shortest_path_length(grid)
        return shortest_path_length

    def test_given_1(self):
        shortest_path_length = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(shortest_path_length, 31)

    def test_input_1(self):
        shortest_path_length = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(shortest_path_length, 468)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        grid = solver.parse_file(input_file_name)
        shortest_scenic_path: int = solver.get_shortest_scenic_path(grid)
        return shortest_scenic_path

    def test_given_2(self):
        shortest_scenic_path = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(shortest_scenic_path, 29)

    def test_input_2(self):
        shortest_scenic_path = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(shortest_scenic_path, 459)


unittest.main(exit=False)
