GIVEN_FILE_NAME = "given_9.txt"
INPUT_FILE_NAME = "input_9.txt"

from enum import Enum


class Move(Enum):
    U = 1
    L = 2
    D = 3
    R = 4


class Point:
    def __init__(self, x: int = None, y: int = None) -> None:
        self.x = x if x is not None else 0
        self.y = y if y is not None else 0

    def perform_move(self, move: Move):
        if move == Move.U:
            self.y += 1
        elif move == Move.L:
            self.x -= 1
        elif move == Move.D:
            self.y -= 1
        else:
            self.x += 1

    def is_point_touching(self, other: "Point") -> bool:
        if (self.x - 1 <= other.x and other.x <= self.x + 1) and (
            self.y - 1 <= other.y and other.y <= self.y + 1
        ):
            return True
        return False

    def move_to_meet(self, other: "Point") -> None:
        if self.is_point_touching(other):
            return
        if self.x == other.x:
            if self.y < other.y:
                self.y += 1
            else:
                self.y -= 1
        elif self.y == other.y:
            if self.x < other.x:
                self.x += 1
            else:
                self.x -= 1
        elif self.x < other.x and self.y < other.y:
            self.x += 1
            self.y += 1
        elif self.x < other.x and self.y > other.y:
            self.x += 1
            self.y -= 1
        elif self.x > other.x and self.y < other.y:
            self.x -= 1
            self.y += 1
        else:
            self.x -= 1
            self.y -= 1

    def __repr__(self) -> str:
        return "x: {}, y: {}".format(self.x, self.y)


class Solver:
    MOVE_DICT = {"U": Move.U, "L": Move.L, "D": Move.D, "R": Move.R}

    def parse_file(self, input_file_name: str) -> "list[Move]":
        list_of_moves: list[Move] = []
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                move_raw, number = stripped_line.split()
                for _ in range(int(number)):
                    list_of_moves.append(self.MOVE_DICT[move_raw])
        return list_of_moves

    def get_number_of_traveled_positions(
        self,
        list_of_moves: "list[Move]",
        number_of_knots: int = 0,
    ) -> None:
        chain = (
            [Point(0, 0)]
            + [Point(0, 0) for _ in range(number_of_knots - 2)]
            + [Point(0, 0)]
        )
        tail_traveled_positions: set[str] = set(
            ["x" + str(chain[-1].x) + "y" + str(chain[-1].y)]
        )
        for move in list_of_moves:
            chain[0].perform_move(move)
            for i in range(len(chain) - 1):
                if not chain[i].is_point_touching(chain[i + 1]):
                    chain[i + 1].move_to_meet(chain[i])
            tail_traveled_positions.add("x" + str(chain[-1].x) + "y" + str(chain[-1].y))
        return len(tail_traveled_positions)


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_moves: list[Move] = solver.parse_file(input_file_name)
        number_of_traveled_positions = solver.get_number_of_traveled_positions(
            list_of_moves
        )
        return number_of_traveled_positions

    def test_given_1(self):
        number_of_traveled_positions = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(number_of_traveled_positions, 88)

    def test_input_1(self):
        number_of_traveled_positions = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(number_of_traveled_positions, 6563)
        return

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_moves: list[Move] = solver.parse_file(input_file_name)
        number_of_traveled_positions = solver.get_number_of_traveled_positions(
            list_of_moves, 10
        )
        return number_of_traveled_positions

    def test_given_2(self):
        number_of_traveled_positions = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(number_of_traveled_positions, 36)

    def test_input_2(self):
        number_of_traveled_positions = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(number_of_traveled_positions, 2653)
        return


unittest.main(exit=False)
