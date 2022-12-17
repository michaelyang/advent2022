GIVEN_FILE_NAME = "given_15.txt"
INPUT_FILE_NAME = "input_15.txt"

from typing import Tuple


class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def distance(self, other: "Point") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def merge(self, intervals):
        if len(intervals) == 0 or len(intervals) == 1:
            return intervals
        intervals.sort(key=lambda x: x[0])
        # print(intervals)
        result = [intervals[0]]
        for interval in intervals[1:]:
            if interval[0] <= result[-1][1] + 1:
                # print("merging {} with {}".format(interval, result[-1]))
                result[-1][1] = max(result[-1][1], interval[1])
            else:
                result.append(interval)
        # print(result)
        return result

    def get_all_points_distance_away(
        self, distance: int, min_x, max_x, min_y, max_y, row_dict: set
    ) -> None:
        # maybe i return for each y a range of x
        # (-x to x)
        # print("This is for ({},{}) with distance {}".format(self.x, self.y, distance))
        for i in range(distance + 1):
            left = min(max(min_x, self.x - distance + i), max_x)
            right = min(max(min_x, self.x + distance - i), max_x)
            top = self.y + i
            bottom = self.y - i
            """
            print(
                "left: {}, right: {}, top: {}, bottom: {}".format(
                    left, right, top, bottom
                )
            )"""
            interval = [left, right]
            if top >= min_y and top <= max_y:
                if top in row_dict:
                    intervals_top = row_dict[top]
                    intervals_top.append(interval)
                    merged_intervals_top = self.merge(intervals_top)
                    row_dict[top] = merged_intervals_top
                else:
                    row_dict[top] = [interval]
            interval = [left, right]
            if bottom >= min_y and bottom <= max_y and top != bottom:
                if bottom in row_dict:
                    intervals_bottom = row_dict[bottom]
                    intervals_bottom.append(interval)
                    merged_intervals_bottom = self.merge(intervals_bottom)
                    row_dict[bottom] = merged_intervals_bottom
                else:
                    row_dict[bottom] = [interval]
        """
        for y in range(min_y, max_y + 1):
            row_to_print = []
            if y not in row_dict:
                row_to_print.extend(["." * (max_x - min_x + 1)])
            else:
                row = row_dict[y]
                last_end = 0
                for interval in row:
                    start, end = interval
                    if start - last_end > 0:
                        row_to_print.extend(["." * (start - last_end)])
                    row_to_print.extend(["#" * (end - start + 1)])
                    last_end = end + 1
                if last_end < max_x:
                    row_to_print.extend(["." * (max_x - last_end + 1)])
        """
        """
        for x_diff in range(distance + 1):
            plus_x = self.x + x_diff
            minus_x = self.x - x_diff
            y_diff = distance - x_diff
            if (
                min_x <= plus_x
                and plus_x <= max_x
                and min_x <= minus_x
                and minus_x <= max_x
            ):
                for y in range(
                    max(self.y - y_diff, min_y), min(self.y + y_diff + 1, max_y + 1)
                ):
                    points_set.discard(Point(plus_x, y))
                    if plus_x != minus_x:
                        points_set.discard(Point(minus_x, y))
            elif min_x <= plus_x and plus_x <= max_x:
                for y in range(
                    max(self.y - y_diff, min_y), min(self.y + y_diff + 1, max_y + 1)
                ):
                    points_set.discard(Point(plus_x, y))
            elif min_x <= minus_x and minus_x <= max_x:
                for y in range(
                    max(self.y - y_diff, min_y), min(self.y + y_diff + 1, max_y + 1)
                ):
                    points_set.discard(Point(minus_x, y))
        """

    def __repr__(self) -> str:
        return "({}, {})".format(self.x, self.y)

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x) and (self.y == other.y)
        else:
            return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class Map:
    def __init__(self):
        self.source_distance_list: Tuple(Point, int) = []
        self.occupied_point_set = set()
        self.min_x = None
        self.max_x = None

    def add_source_beacon(self, source: Point, beacon: Point) -> None:
        distance: int = beacon.distance(source)
        self.source_distance_list.append((source, distance))
        if not self.min_x or (source.x - distance) < self.min_x:
            self.min_x = source.x - distance
        if not self.max_x or (source.x + distance) > self.max_x:
            self.max_x = source.x + distance
        self.occupied_point_set.add(beacon)
        self.occupied_point_set.add(source)

    def is_point_in_source_range(self, point: Point) -> bool:
        for source_distance in self.source_distance_list:
            source, distance = source_distance
            if source.distance(point) <= distance:
                return True
        return False

    def number_of_points_covered_in_row(self, y: int) -> int:
        count: int = 0
        for x in range(self.min_x, self.max_x):
            if (
                self.is_point_in_source_range(Point(x, y))
                and Point(x, y) not in self.occupied_point_set
            ):
                count += 1
        return count


class Solver:
    def parse_file(self, input_file_name: str) -> Map:
        map = Map()
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                sensor_raw, beacon_raw = stripped_line.split(":")
                sensor_x_raw, sensor_y_raw = sensor_raw.replace("Sensor at ", "").split(
                    ", "
                )
                beacon_x_raw, beacon_y_raw = beacon_raw.replace(
                    "closest beacon is at ", ""
                ).split(", ")
                sensor_x: int = int(sensor_x_raw.replace("x=", ""))
                sensor_y: int = int(sensor_y_raw.replace("y=", ""))
                beacon_x: int = int(beacon_x_raw.replace("x=", ""))
                beacon_y: int = int(beacon_y_raw.replace("y=", ""))
                sensor: Point = Point(sensor_x, sensor_y)
                beacon: Point = Point(beacon_x, beacon_y)
                map.add_source_beacon(sensor, beacon)
        return map

    def get_tuning_frequency(self, map: Map, search_min: int, search_max: int) -> int:
        """
        points_to_check = set()
        for x in range(search_min, search_max + 1):
            for y in range(search_min, search_max + 1):
                if not map.is_point_in_source_range(Point(x, y)):
                    return (x * 4000000) + y
        """
        """
        for x in range(search_min, search_max + 1):
            for y in range(search_min, search_max + 1):
                points_to_check.add(Point(x, y))
        
        for source_distance in map.source_distance_list:
            source, distance = source_distance
            source.remove_all_points_distance_away(
                distance,
                search_min,
                search_max,
                search_min,
                search_max,
                row_dict,
            )
        point = points_to_check.pop()
        return (point.x * 4000000) + point.y
        """
        row_dict = dict()
        for source_distance in map.source_distance_list:
            source, distance = source_distance
            source.get_all_points_distance_away(
                distance,
                search_min,
                search_max,
                search_min,
                search_max,
                row_dict,
            )
        for y in range(search_min, search_max + 1):
            x = None
            row_internvals = row_dict[y]
            if len(row_internvals) > 1:
                x = row_internvals[0][1] + 1
            elif row_internvals[0][0] > search_min:
                x = search_min
            elif row_internvals[0][1] < search_max:
                x = search_max
            if x:
                return (x * 4000000) + y


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str, y: int) -> int:
        solver = Solver()
        map: Map = solver.parse_file(input_file_name)
        number_of_points_covered = map.number_of_points_covered_in_row(y)
        return number_of_points_covered

    def test_given_1(self):
        number_of_points_covered = self.solve_1(GIVEN_FILE_NAME, 10)
        self.assertEqual(number_of_points_covered, 26)

    def test_input_1(self):
        number_of_points_covered = self.solve_1(INPUT_FILE_NAME, 2000000)
        self.assertEqual(number_of_points_covered, 4919281)

    def solve_2(self, input_file_name: str, search_min: int, search_max: int) -> int:
        solver = Solver()
        map: Map = solver.parse_file(input_file_name)
        tuning_frequency = solver.get_tuning_frequency(map, search_min, search_max)
        return tuning_frequency

    def test_given_2(self):
        tuning_frequency = self.solve_2(GIVEN_FILE_NAME, 0, 20)
        self.assertEqual(tuning_frequency, 56000011)

    def test_input_2(self):
        tuning_frequency = self.solve_2(INPUT_FILE_NAME, 0, 4000000)
        self.assertEqual(tuning_frequency, 12630143363767)


unittest.main(exit=False)
