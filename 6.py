GIVEN_FILE_NAME = "given_6.txt"
INPUT_FILE_NAME = "input_6.txt"


class DatastreamBuffer:
    def __init__(self, value: str) -> None:
        self.value = value

    def get_first_marker_index(self, length_of_sequence: int = 4) -> int:
        current_index = length_of_sequence
        while current_index < len(self.value):
            sequence: str = self.value[
                current_index - length_of_sequence : current_index
            ]
            if len(set(sequence)) == length_of_sequence:
                return current_index
            current_index += 1
        return -1

    def __repr__(self) -> str:
        return self.value


class Solver:
    def parse_file(self, input_file_name: str) -> DatastreamBuffer:
        datastream_buffer: DatastreamBuffer
        with open(input_file_name) as f:
            for line in f:
                datastream_buffer = DatastreamBuffer(line)
        return datastream_buffer


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        datastream_buffer = solver.parse_file(input_file_name)
        return datastream_buffer.get_first_marker_index(4)

    def test_given_1(self):
        first_marker_index = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(first_marker_index, 7)

    def test_input_1(self):
        first_marker_index = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(first_marker_index, 1538)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        datastream_buffer = solver.parse_file(input_file_name)
        return datastream_buffer.get_first_marker_index(14)

    def test_given_2(self):
        first_marker_index = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(first_marker_index, 19)

    def test_input_2(self):
        first_marker_index = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(first_marker_index, 2315)


unittest.main(exit=False)
