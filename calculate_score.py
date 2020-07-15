from gamegui import game


class Scorer:
    """Inherits roll result from turn and defines functions for detecting and scoring roll results. Contains algorithms for each scoring category
    to either award points or grant 0 points if a roll does not meet the requirements"""

    def __init__(self, roll_result, score_board):
        """Takes the roll result from Yahtzee.py and uses it for scoring and defines dicts for filtering and applying singleScores and
        for detecting transferring user category get_selection into the category_function_dict list of functions. Also sets up the board to be used as a class parameter"""
        self.roll_result = roll_result
        self.singles = {
            "ones": 1,
            "twos": 2,
            "threes": 3,
            "fours": 4,
            "fives": 5,
            "sixes": 6,
        }
        self.category_function_dict = {
            "ones": self.single_die_score,
            "twos": self.single_die_score,
            "threes": self.single_die_score,
            "fours": self.single_die_score,
            "fives": self.single_die_score,
            "sixes": self.single_die_score,
            "three of a kind": self.three_of_a_kind,
            "four of a kind": self.four_of_a_kind,
            "full house": self.full_house,
            "small straight": self.small_straight,
            "large straight": self.large_straight,
            "yahtzee": self.yathzee,
            "chance": self.chance,
        }
        self.score_board = score_board
        self.game = game

    def score_roll(self, user_category_selection):
        """Expects user_category_selection and assigns it as a Scorer class variable.
        Checks if the user_category_selection is a yahtzee and if there is already a scored yahtzee.
            If so it applies a bonus yahtzee score.
        Checks if the user_category_selection has been called before and is no longer None.
            If so,it assigns the corresponding roll function to the players score dict."""
        self.user_category_selection = user_category_selection
        if self.is_yahtzee() and (
            self.score_board.score_board_dict["yahtzee"] != None
            and self.score_board.score_board_dict["yahtzee"] != 0
        ):
            self.score_board.score_board_dict["yahtzee bonus"] += 100
        if self.score_board.score_board_dict[user_category_selection] is None:
            self.score_board.score_board_dict[
                user_category_selection
            ] = self.category_function_dict[user_category_selection]()
            self.game.player_scores[
                user_category_selection
            ] = self.category_function_dict[user_category_selection]()

        self.game.update_idletasks()

    def single_die_score(self):
        """Parses singles dict then adds sum of the singles roll result to the scoring dictionary"""
        if self.user_category_selection in self.singles:
            score = sum(
                i
                for i in self.roll_result
                if i == self.singles[self.user_category_selection]
            )
        else:
            score = 0
        return score

    def three_of_a_kind(self):
        """Algorithm to detect at least three dice the same"""
        self.roll_result.sort()
        if (
            self.roll_result[0] == self.roll_result[2]
            or self.roll_result[1] == self.roll_result[3]
            or self.roll_result[2] == self.roll_result[4]
        ):
            score = sum(self.roll_result)
        else:
            score = 0

        return score

    def four_of_a_kind(self):
        """Algorithm to detect at least four dice the same"""
        self.roll_result.sort()
        if (
            self.roll_result[0] == self.roll_result[3]
            or self.roll_result[1] == self.roll_result[4]
        ):
            score = sum(self.roll_result)
        else:
            score = 0

        return score

    def full_house(self):
        """Algorithm to detect three of one number and two of another"""
        self.roll_result.sort()
        if len(set(self.roll_result)) != 2:
            score = 0
        elif (
            self.roll_result[0] != self.roll_result[3]
            and self.roll_result[1] != self.roll_result[4]
        ):
            score = 25
        else:
            score = 0

        return score

    def small_straight(self):
        """Algorithm to detect four sequential dice"""
        self.roll_result.sort()
        if len(set(self.roll_result)) < 4:
            score = 0
        elif (
            (len(set([1, 2, 3, 4]).intersection(set(self.roll_result))) == 4)
            or (len(set([2, 3, 4, 5]).intersection(set(self.roll_result))) == 4)
            or (len(set([3, 4, 5, 6]).intersection(set(self.roll_result))) == 4)
        ):
            score = 30
        else:
            score = 0

        return score

    def large_straight(self):
        """Algorithm to detect five sequential dice"""
        self.roll_result.sort()
        if len(set(self.roll_result)) < 5:
            score = 0
        elif (len(set([1, 2, 3, 4, 5]).intersection(set(self.roll_result))) == 5) or (
            len(set([2, 3, 4, 5, 6]).intersection(set(self.roll_result))) == 5
        ):
            score = 40
        else:
            score = 0

        return score

    def yathzee(self):
        """Algorithm to detect that all five dice are the same"""
        if len(set(self.roll_result)) == 1:
            if self.score_board.score_board_dict["yahtzee"] is None:
                score = 50
                return score
        else:
            score = 0
            return score

    def is_yahtzee(self):
        """Function used to check if any given roll is a Yahtzee(all five dice are the same)."""
        return len(set(self.roll_result)) == 1

    def chance(self):
        """Algorithm to compute any combination of roll result"""
        return sum(self.roll_result)
