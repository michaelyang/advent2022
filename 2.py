GIVEN_FILE_NAME = "given_2.txt"
INPUT_FILE_NAME = "input_2.txt"

from enum import Enum


class HandShape(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


class MatchResult(Enum):
    WIN = 0
    DRAW = 1
    LOSE = 2


class Match:
    def __init__(self, player_hand: HandShape, opponent_hand: HandShape) -> None:
        self.player_hand = player_hand
        self.opponent_hand = opponent_hand

    def get_match_result(self) -> MatchResult:
        if self.player_hand is self.opponent_hand:
            return MatchResult.DRAW
        elif self.did_player_win(self.player_hand, self.opponent_hand):
            return MatchResult.WIN
        else:
            return MatchResult.LOSE

    def did_player_win(self, player_hand: HandShape, opponent_hand: HandShape) -> bool:
        if Match.get_winning_hand(opponent_hand) is player_hand:
            return True
        return False

    def get_winning_hand(opponent_hand: HandShape) -> HandShape:
        if opponent_hand is HandShape.ROCK:
            return HandShape.PAPER
        elif opponent_hand is HandShape.PAPER:
            return HandShape.SCISSORS
        else:
            return HandShape.ROCK

    def get_losing_hand(opponent_hand: HandShape) -> HandShape:
        if opponent_hand is HandShape.ROCK:
            return HandShape.SCISSORS
        elif opponent_hand is HandShape.PAPER:
            return HandShape.ROCK
        else:
            return HandShape.PAPER


class Game:
    HAND_SCORE_DICT = {HandShape.ROCK: 1, HandShape.PAPER: 2, HandShape.SCISSORS: 3}
    MATCH_LOSE_SCORE = 0
    MATCH_DRAW_SCORE = 3
    MATCH_WIN_SCORE = 6

    def __init__(self) -> None:
        self.player_score = 0

    def get_score(self):
        return self.player_score

    def play_match(self, match: Match) -> None:
        hand_score = self.HAND_SCORE_DICT[match.player_hand]
        outcome_score = self._get_match_outcome_score(match)
        self.player_score += hand_score + outcome_score
        return

    def _get_match_outcome_score(self, match: Match) -> int:
        match_result: MatchResult = match.get_match_result()
        if match_result is MatchResult.DRAW:
            return self.MATCH_DRAW_SCORE
        elif match_result is MatchResult.WIN:
            return self.MATCH_WIN_SCORE
        else:
            return self.MATCH_LOSE_SCORE


class Solver:
    def parse_file_1(self, input_file_name: str) -> "list[Match]":
        SEPARATOR_CHARACTER = " "
        OPPONENT_PARSE_DICT = {
            "A": HandShape.ROCK,
            "B": HandShape.PAPER,
            "C": HandShape.SCISSORS,
        }
        PLAYER_PARSE_DICT = {
            "X": HandShape.ROCK,
            "Y": HandShape.PAPER,
            "Z": HandShape.SCISSORS,
        }
        list_of_matches: list[Match] = []
        with open(input_file_name) as f:
            for line in f:
                opponent_hand_raw, player_hand_raw = line.strip().split(
                    SEPARATOR_CHARACTER
                )
                opponent_hand: HandShape = OPPONENT_PARSE_DICT[opponent_hand_raw]
                player_hand: HandShape = PLAYER_PARSE_DICT[player_hand_raw]
                list_of_matches.append(Match(player_hand, opponent_hand))
        return list_of_matches

    def parse_file_2(self, input_file_name: str) -> "list[Match]":
        SEPARATOR_CHARACTER = " "
        OPPONENT_PARSE_DICT = {
            "A": HandShape.ROCK,
            "B": HandShape.PAPER,
            "C": HandShape.SCISSORS,
        }
        MATCH_RESULT_PRASE_DICT = {
            "X": MatchResult.LOSE,
            "Y": MatchResult.DRAW,
            "Z": MatchResult.WIN,
        }
        list_of_matches: list[Match] = []
        with open(input_file_name) as f:
            for line in f:
                opponent_hand_raw, match_result_raw = line.strip().split(
                    SEPARATOR_CHARACTER
                )
                opponent_hand: HandShape = OPPONENT_PARSE_DICT[opponent_hand_raw]
                match_result: MatchResult = MATCH_RESULT_PRASE_DICT[match_result_raw]
                player_hand: HandShape = self.get_player_hand(
                    opponent_hand, match_result
                )
                list_of_matches.append(Match(player_hand, opponent_hand))
        return list_of_matches

    def get_total_score(self, list_of_matches: "list[Match]") -> int:
        game = Game()
        for match in list_of_matches:
            game.play_match(match)
        return game.get_score()

    def get_player_hand(
        self, opponent_hand: HandShape, match_result: MatchResult
    ) -> HandShape:
        if match_result is MatchResult.DRAW:
            return opponent_hand
        elif match_result is MatchResult.WIN:
            return Match.get_winning_hand(opponent_hand)
        else:
            return Match.get_losing_hand(opponent_hand)


import unittest


class SolverTest(unittest.TestCase):
    def solve_1(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_matches: list[Match] = solver.parse_file_1(input_file_name)
        total_score = solver.get_total_score(list_of_matches)
        return total_score

    def test_given_1(self):
        total_score = self.solve_1(GIVEN_FILE_NAME)
        self.assertEqual(total_score, 15)

    def test_input_1(self):
        total_score = self.solve_1(INPUT_FILE_NAME)
        self.assertEqual(total_score, 8933)

    def solve_2(self, input_file_name: str) -> int:
        solver = Solver()
        list_of_matches: list[Match] = solver.parse_file_2(input_file_name)
        total_score = solver.get_total_score(list_of_matches)
        return total_score

    def test_given_2(self):
        total_score = self.solve_2(GIVEN_FILE_NAME)
        self.assertEqual(total_score, 12)

    def test_input_2(self):
        total_score = self.solve_2(INPUT_FILE_NAME)
        self.assertEqual(total_score, 11998)


unittest.main(exit=False)
