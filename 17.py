GIVEN_FILE_NAME = "given_17.txt"
INPUT_FILE_NAME = "input_17.txt"

from enum import Enum


class RockShape(Enum):
    HORIZONTAL_L = 0
    VERTICAL_L = 1
    PLUS = 2
    SQUARE = 3
    RIGHT_ANGLE = 4


class WindDirection(Enum):
    LEFT = 0
    RIGHT = 1


class Point:
    def __init__(self, x: int = None, y: int = None) -> None:
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0

    def __repr__(self) -> str:
        return "({}, {})".format(self.x, self.y)


class Chamber:
    CHAMBER_WIDTH = 7

    def __init__(self, list_of_wind_directions: "list[WindDirection]") -> None:
        self.chamber: list[list] = [["."] * self.CHAMBER_WIDTH for _ in range(3)]
        self.wind: list[WindDirection] = list_of_wind_directions
        self.current_wind_index = 0

    def get_current_height(self) -> int:
        return self.get_current_y() + 1

    def get_current_y(self) -> int:
        for i in range(len(self.chamber) - 1, -1, -1):
            row = self.chamber[i]
            for item in row:
                if item == "#":
                    return i
        return -1

    def add_chamber_height(self, rock_height) -> None:
        current_rock_height = self.get_current_y()
        current_chamber_height = len(self.chamber)
        available_gap = current_chamber_height - current_rock_height - 1
        number_of_rows_to_add = 3 + rock_height - available_gap
        if number_of_rows_to_add > 0:
            self.chamber.extend(
                [["."] * self.CHAMBER_WIDTH for _ in range(number_of_rows_to_add)]
            )
        elif number_of_rows_to_add < 0:
            for _ in range(abs(number_of_rows_to_add)):
                self.chamber.pop()

    def add_rock(self, rock_shape: RockShape) -> None:
        if rock_shape == RockShape.HORIZONTAL_L:
            self.add_chamber_height(1)
            # print(self.__repr__())
            points = [
                Point(2, len(self.chamber) - 1),
                Point(3, len(self.chamber) - 1),
                Point(4, len(self.chamber) - 1),
                Point(5, len(self.chamber) - 1),
            ]
        elif rock_shape == RockShape.VERTICAL_L:
            self.add_chamber_height(4)
            # print(self.__repr__())
            points = [
                Point(2, len(self.chamber) - 1),
                Point(2, len(self.chamber) - 2),
                Point(2, len(self.chamber) - 3),
                Point(2, len(self.chamber) - 4),
            ]
        elif rock_shape == RockShape.PLUS:
            self.add_chamber_height(3)
            # print(self.__repr__())
            points = [
                Point(3, len(self.chamber) - 1),
                Point(2, len(self.chamber) - 2),
                Point(3, len(self.chamber) - 2),
                Point(4, len(self.chamber) - 2),
                Point(3, len(self.chamber) - 3),
            ]
        elif rock_shape == RockShape.SQUARE:
            self.add_chamber_height(2)
            # print(self.__repr__())
            points = [
                Point(2, len(self.chamber) - 1),
                Point(3, len(self.chamber) - 1),
                Point(2, len(self.chamber) - 2),
                Point(3, len(self.chamber) - 2),
            ]
        elif rock_shape == RockShape.RIGHT_ANGLE:
            self.add_chamber_height(3)
            # print(self.__repr__())
            points = [
                Point(2, len(self.chamber) - 3),
                Point(3, len(self.chamber) - 3),
                Point(4, len(self.chamber) - 1),
                Point(4, len(self.chamber) - 2),
                Point(4, len(self.chamber) - 3),
            ]
        if not points:
            return
        while True:
            current_wind: WindDirection = self.wind[
                self.current_wind_index % len(self.wind)
            ]
            if current_wind == WindDirection.LEFT:
                new_points = [Point(point.x - 1, point.y) for point in points]
                # print("trying to move left to {}".format(new_points))
            elif current_wind == WindDirection.RIGHT:
                new_points = [Point(point.x + 1, point.y) for point in points]
                # print("trying to move right to {}".format(new_points))
            if self.are_points_available(new_points):
                # print("moving to {}".format(new_points))
                points = new_points
            self.current_wind_index += 1
            down_points = [Point(point.x, point.y - 1) for point in points]
            # print("trying to move down to {}".format(down_points))
            if self.are_points_available(down_points):
                # print("moving to {}".format(down_points))
                points = down_points
            else:
                self.occupy_points(points)
                """print(self.__repr__())
                print("\n")"""
                break

    def are_points_available(self, points: "list[Point]") -> bool:
        for point in points:
            if point.x < 0 or point.x >= self.CHAMBER_WIDTH or point.y < 0:
                return False
            if self.get_item_at_point(point) == "#":
                return False
        return True

    def get_item_at_point(self, point: Point):
        return self.chamber[point.y][point.x]

    def occupy_points(self, points: "list[Point]") -> None:
        # print("occupying: {}".format(points))
        for point in points:
            self.chamber[point.y][point.x] = "#"

    def __repr__(self) -> str:
        return "\n".join(["".join(row) for row in self.chamber[::-1]])


class Solver:
    def parse_file(self, input_file_name: str) -> Chamber:
        list_of_wind_directions: list[WindDirection] = []
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                for wind_direction_raw in stripped_line:
                    if wind_direction_raw == "<":
                        list_of_wind_directions.append(WindDirection.LEFT)
                    elif wind_direction_raw == ">":
                        list_of_wind_directions.append(WindDirection.RIGHT)
        return Chamber(list_of_wind_directions)

    def get_height_after_n_rocks(self, chamber: Chamber, number_of_rocks: int) -> int:
        list_of_rock_shapes: list[RockShape] = [
            RockShape.HORIZONTAL_L,
            RockShape.PLUS,
            RockShape.RIGHT_ANGLE,
            RockShape.VERTICAL_L,
            RockShape.SQUARE,
        ]

        for i in range(number_of_rocks):
            rock_shape: RockShape = list_of_rock_shapes[i % len(list_of_rock_shapes)]
            chamber.add_rock(rock_shape)
        return chamber.get_current_height()


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        chamber = solver.parse_file(input_file_name)
        height = solver.get_height_after_n_rocks(chamber, 2022)
        return height

    def test_given_1(self):
        height = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(height, 3068)

    def test_input_1(self):
        height = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(height, 3135)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        chamber = solver.parse_file(input_file_name)
        height = solver.get_height_after_n_rocks(chamber, 1000000)
        return height

    def test_given_2(self):
        height = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(height, 1514285714288)

    def test_input_2(self):
        height = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(height, 3135)


unittest.main(exit=False)
