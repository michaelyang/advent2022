GIVEN_FILE_NAME = "given_4.txt"
INPUT_FILE_NAME = "input_4.txt"


class Assignment:
    def __init__(self, start: int, end: int) -> None:
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return "{}-{}".format(self.start, self.end)


class Pair:
    def __init__(self, assignment1: Assignment, assignment2: Assignment) -> None:
        self.assignment1 = assignment1
        self.assignment2 = assignment2

    def do_assignments_overlap_fully(self) -> bool:
        is_assignment1_contained: bool = (
            self.assignment1.start >= self.assignment2.start
            and self.assignment1.end <= self.assignment2.end
        )
        is_assignment2_contained: bool = (
            self.assignment2.start >= self.assignment1.start
            and self.assignment2.end <= self.assignment1.end
        )
        return is_assignment1_contained or is_assignment2_contained

    def do_assignments_overlap_partially(self) -> bool:
        is_end_of_assignment1_overlapping: bool = (
            self.assignment1.end >= self.assignment2.start
            and self.assignment1.end <= self.assignment2.end
        )
        is_beginning_of_assignment1_overlapping: bool = (
            self.assignment1.start <= self.assignment2.end
            and self.assignment1.start >= self.assignment2.start
        )
        return (
            self.do_assignments_overlap_fully()
            or is_end_of_assignment1_overlapping
            or is_beginning_of_assignment1_overlapping
        )


class Solver:
    PAIR_SEPARATOR = ","
    ASSIGNMENT_SEPARATOR = "-"

    def parse_file(self, input_file_name: str) -> "list[Pair]":
        list_of_pairs: list[Pair] = []
        with open(input_file_name) as f:
            for line in f:
                assignment1_raw, assignment2_raw = line.split(self.PAIR_SEPARATOR)
                assignment1_start_raw, assignment1_end_raw = assignment1_raw.split(
                    self.ASSIGNMENT_SEPARATOR
                )
                assignment2_start_raw, assignment2_end_raw = assignment2_raw.split(
                    self.ASSIGNMENT_SEPARATOR
                )
                pair = Pair(
                    Assignment(int(assignment1_start_raw), int(assignment1_end_raw)),
                    Assignment(int(assignment2_start_raw), int(assignment2_end_raw)),
                )
                list_of_pairs.append(pair)
        return list_of_pairs

    def get_number_of_fully_overlapping_pairs(self, list_of_pairs: "list[Pair]") -> int:
        return len(
            list(
                filter(lambda pair: pair.do_assignments_overlap_fully(), list_of_pairs)
            )
        )

    def get_number_of_partially_overlapping_pairs(
        self, list_of_pairs: "list[Pair]"
    ) -> int:
        return len(
            list(
                filter(
                    lambda pair: pair.do_assignments_overlap_partially(), list_of_pairs
                )
            )
        )


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_pairs: list[Pair] = solver.parse_file(input_file_name)
        return solver.get_number_of_fully_overlapping_pairs(list_of_pairs)

    def test_given_1(self):
        number_of_fully_overlapping_pairs = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(number_of_fully_overlapping_pairs, 2)

    def test_input_1(self):
        number_of_fully_overlapping_pairs = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(number_of_fully_overlapping_pairs, 487)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_pairs: list[Pair] = solver.parse_file(input_file_name)
        return solver.get_number_of_partially_overlapping_pairs(list_of_pairs)

    def test_given_2(self):
        number_of_partially_overlapping_pairs = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(number_of_partially_overlapping_pairs, 4)

    def test_input_2(self):
        number_of_partially_overlapping_pairs = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(number_of_partially_overlapping_pairs, 849)


unittest.main(exit=False)
