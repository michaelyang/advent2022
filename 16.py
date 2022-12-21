GIVEN_FILE_NAME = "given_16.txt"
INPUT_FILE_NAME = "input_16.txt"

from typing import Tuple


class Valve:
    def __init__(self, name: str, flow_rate: int):
        self.name: str = name
        self.flow_rate: int = flow_rate
        self.connected_valve: list["str"] = []

    def add_connected_valves(self, valves: "list[str]") -> None:
        self.connected_valve.extend(valves)

    def __repr__(self) -> str:
        return "Valve {} has flow rate={}; tunnels lead to valves {}".format(
            self.name, str(self.flow_rate), ", ".join(self.connected_valve)
        )


class Solver:
    def parse_file(self, input_file_name: str) -> dict:
        valve_dict = dict()
        with open(input_file_name) as f:
            for line in f:
                stripped_line: str = line.strip()
                valve_raw, connection_raw = stripped_line.split(";")
                name_raw, flow_rate_raw = (
                    valve_raw.replace("Valve ", "")
                    .replace(" has flow rate", "")
                    .split("=")
                )
                connections = (
                    connection_raw.replace(" tunnels lead to valves ", "")
                    .replace(" tunnel leads to valve ", "")
                    .split(", ")
                )
                valve = Valve(name_raw, int(flow_rate_raw))
                valve.add_connected_valves(connections)
                valve_dict[name_raw] = valve
        return valve_dict

    def get_highest_pressure_release(self, valve_dict: dict, minutes=30) -> int:
        max_released_pressure = None
        non_zero_flow_rate = 0
        for valve in valve_dict.values():
            if valve.flow_rate > 0:
                non_zero_flow_rate += 1
        # dict key to value
        # key is valve, value is max

        valve_set_dict = dict()

        def visit_valve(
            valve: Valve,
            previous_valve: str,
            released_pressure: int,
            current_minute: int,
            opened_valves: set,
        ):
            nonlocal max_released_pressure
            nonlocal minutes
            nonlocal non_zero_flow_rate
            nonlocal valve_set_dict

            # print("In {} at {}".format(valve.name, current_minute))
            if current_minute > minutes - 1 or len(opened_valves) >= non_zero_flow_rate:
                return
            # open the current valve
            if valve.name not in opened_valves and valve.flow_rate > 0:
                opened_valves.add(valve.name)
                minute_after_opening = current_minute + 1
                new_released_pressure = (
                    released_pressure
                    + (minutes - minute_after_opening) * valve.flow_rate
                )
                """
                print(
                    "Opening {} for {}".format(
                        valve.name,
                        released_pressure,
                    )
                )"""
                if (
                    max_released_pressure is None
                    or new_released_pressure >= max_released_pressure
                ):
                    max_released_pressure = new_released_pressure
                frozen_set = frozenset(opened_valves.copy())
                if (
                    frozen_set in valve_set_dict
                    and new_released_pressure > valve_set_dict[frozen_set]
                ):
                    valve_set_dict[frozen_set] = new_released_pressure
                elif frozen_set not in valve_set_dict:
                    valve_set_dict[frozen_set] = new_released_pressure
                visit_valve(
                    valve,
                    "",
                    new_released_pressure,
                    minute_after_opening,
                    opened_valves,
                )
                opened_valves.remove(valve.name)
            # visit connected valve
            valves_to_visit = list(
                filter(
                    lambda valve: valve != previous_valve,
                    valve.connected_valve,
                ),
            )
            for valve_to_visit in valves_to_visit:
                visit_valve(
                    valve_dict[valve_to_visit],
                    valve.name,
                    released_pressure,
                    current_minute + 1,
                    opened_valves,
                )
            return

        visit_valve(valve_dict["AA"], "", 0, 0, set())
        return max_released_pressure, valve_set_dict

    def get_highest_pressure_release_2(self, valve_dict: dict, minutes=26) -> int:
        _, dict = self.get_highest_pressure_release(valve_dict, minutes)
        complete_set = set()
        for key, valve in valve_dict.items():
            if valve.flow_rate > 0:
                complete_set.add(key)
        highest_pressure_release = None
        for key_1, value_1 in dict.items():
            total_pressure_release = value_1
            for key_2, value_2 in dict.items():
                if key_1.intersection(key_2):
                    continue
                total_pressure_release = value_1 + value_2
                if (
                    highest_pressure_release is None
                    or total_pressure_release >= highest_pressure_release
                ):
                    highest_pressure_release = total_pressure_release

        return highest_pressure_release


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        valve_dict = solver.parse_file(input_file_name)
        highest_pressure_release, _ = solver.get_highest_pressure_release(valve_dict)
        return highest_pressure_release

    def test_given_1(self):
        highest_pressure_release = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(highest_pressure_release, 1651)

    def test_input_1(self):
        highest_pressure_release, _ = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(highest_pressure_release, 1940)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        valve_dict = solver.parse_file(input_file_name)
        highest_pressure_release = solver.get_highest_pressure_release_2(valve_dict)
        return highest_pressure_release

    def test_given_2(self):
        highest_pressure_release = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(highest_pressure_release, 1707)

    def test_input_2(self):
        highest_pressure_release = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(highest_pressure_release, 2469)


unittest.main(exit=False)
