GIVEN_FILE_NAME = "given_8.txt"
INPUT_FILE_NAME = "input_8.txt"

from typing import List

class Tree:
    def __init__(self, height: int):
        self.height: int = height

    def __repr__(self):
        return str(self.height)

class Grid:
    def __init__(self):
        self.rows: List[list] = []

    def add_row(self, row: list):
        self.rows.append(row)

    def get_rows(self) -> List[list]:
        return self.rows

    def get_columns(self) -> List[list]:
        return list(map(list, zip(*self.rows)))

    def get_item(self, column, row):
        return self.rows[row][column]

    def __repr__(self):
        return '\n'.join(''.join(str(item) for item in row) for row in self.rows)

class Solver:
    def parse_file(self, input_file_name: str) -> Grid:
        grid = Grid()
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                list_of_trees: list[Tree] = []
                for height_raw in stripped_line:
                    list_of_trees.append(Tree(int(height_raw)))
                grid.add_row(list_of_trees)
        return grid

    def get_number_of_visible_trees(self, grid: Grid) -> int:
        number_of_visible_trees: int = 0
        rows: List[list] = grid.get_rows()
        columns: List[list] = grid.get_columns()
        for i in range(len(columns)):
            for j in range(len(rows)):
                is_on_edge = (i == 0 or i == len(columns) - 1 or j == 0 or j == len(rows) - 1)
                if is_on_edge:
                    number_of_visible_trees += 1
                    continue
                is_visible_from_top = max(tree.height for tree in columns[i][:j]) < grid.get_item(i, j).height
                if is_visible_from_top:
                    number_of_visible_trees += 1
                    continue
                is_visible_from_bottom = max(tree.height for tree in columns[i][j+1:]) < grid.get_item(i, j).height
                if is_visible_from_bottom:
                    number_of_visible_trees += 1
                    continue
                is_visible_from_left = max(tree.height for tree in rows[j][:i]) < grid.get_item(i, j).height
                if is_visible_from_left:
                    number_of_visible_trees += 1
                    continue
                is_visible_from_right = max(tree.height for tree in rows[j][i+1:]) < grid.get_item(i, j).height
                if is_visible_from_right:
                    number_of_visible_trees += 1
                    continue
        return number_of_visible_trees

    def get_highest_scenic_score(self, grid: Grid) -> int:
        highest_scenic_score: int = 0
        rows: List[list] = grid.get_rows()
        columns: List[list] = grid.get_columns()
        for i in range(len(columns)):
            for j in range(len(rows)):
                scenic_score = self.get_scenic_score(grid, i, j)
                if scenic_score > highest_scenic_score:
                    highest_scenic_score = scenic_score
        return highest_scenic_score

    def get_scenic_score(self, grid: Grid, column: int, row: int) -> int:
        rows: List[list] = grid.get_rows()
        columns: List[list] = grid.get_columns()
        is_on_edge = (column == 0 or column == len(columns) - 1 or row == 0 or row == len(rows) - 1)
        if is_on_edge:
            return 0
        up_score = 0
        down_score = 0
        left_score = 0
        right_score = 0
        trees_to_the_top = columns[column][:row]
        for tree in trees_to_the_top[::-1]:
            up_score += 1
            if tree.height >= grid.get_item(column, row).height:
                pass
        trees_to_the_bottom = columns[column][row+1:]
        for tree in trees_to_the_bottom:
            down_score += 1
            if tree.height >= grid.get_item(column, row).height:
                pass
        trees_to_the_left = rows[row][:column]
        for tree in trees_to_the_left[::-1]:
            left_score += 1
            if tree.height >= grid.get_item(column, row).height:
                pass
        trees_to_the_right = rows[row][column+1:]

        for tree in trees_to_the_right:
            right_score += 1
            if tree.height >= grid.get_item(column, row).height:
                pass
        print(left_score)
        print(right_score)
        print(up_score)
        print(down_score)
        return left_score * right_score * up_score * down_score

import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        grid = solver.parse_file(input_file_name)
        number_of_visible_trees: int = solver.get_number_of_visible_trees(grid)
        return number_of_visible_trees

    def test_given_1(self):
        number_of_visible_trees = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(number_of_visible_trees, 21)

    def test_input_1(self):
        number_of_visible_trees = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(number_of_visible_trees, 1870)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        grid = solver.parse_file(input_file_name)
        highest_scenic_score: int = solver.get_highest_scenic_score(grid)
        return highest_scenic_score

    def test_given_2(self):
        highest_scenic_score = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(highest_scenic_score, 8)

    def test_input_2(self):
        #highest_scenic_score = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(highest_scenic_score, 1870)

unittest.main(exit=False)
