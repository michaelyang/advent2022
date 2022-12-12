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
        if row >= len(row) or column >= len(row[0]):
            return None
        return self.rows[row][column]

    def set_starting_point(self, column:int, row:int):
        self.starting_point = (column, row)

    def set_ending_point(self, column:int, row:int):
        self.ending_point = (column, row)

    def __repr__(self):
        return "\n".join("".join(str(item) for item in row) for row in self.rows)


class Solver:
    STARTING_POINT = 'S'
    ENDING_POINT = 'E'
    def parse_file(self, input_file_name: str) -> Grid:
        grid = Grid()
        current_row = 0
        with open(input_file_name) as f:
            current_column = 0
            for line in f:
                stripped_line: str = line.strip()
                list_of_elevations: list[str] = []
                for elevation_raw in stripped_line:
                    if (elevation_raw == self.STARTING_POINT):
                        list_of_elevations.append('a')
                        grid.set_starting_point(current_column, current_row)
                    elif (elevation_raw == self.ENDING_POINT):
                        list_of_elevations.append('z')
                        grid.set_ending_point(current_column, current_row)
                    else:
                        list_of_elevations.append(elevation_raw)
                    current_column += 1
                grid.add_row(list_of_elevations)
                current_column = 0
                current_row += 1
        return grid

    def get_shortest_path_length(self, grid:Grid) -> int:
        starting_column, starting_row = grid.starting_point
        points_to_visit = [(starting_column, starting_row, 0)]
        visited_points = set()
        while points_to_visit:
            current_column, current_row, length_so_far = points_to_visit.pop(0)
            # Top
            top_elevation = grid.get_item(current_column, current_row-1)
            if top_elevation and ord(top_elevation + 1) >:

            # Left
            # Bottom
            # Right
            if
        return -1

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
        self.assertEqual(shortest_path_length, 1870)


unittest.main(exit=False)
