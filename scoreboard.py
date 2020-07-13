import tkinter as tk
from gamegui import GameGui, game


class ScoreKeeper:
    """This is the class for keeping track of the active scores and the formulation of what the categories are.
    It keeps the algorithms for the upper score bonus, end of game score and displaying the actively entered categories during a given turn"""

    def __init__(self):
        """Initializes the ScoreKeeper class to have a dictionary for each scoring category defaulted to None as well as the scord_board_upper_list tuple"""
        self.game = game
        self.score_board_dict = {
            "ones": None,
            "twos": None,
            "threes": None,
            "fours": None,
            "fives": None,
            "sixes": None,
            "three of a kind": None,
            "four of a kind": None,
            "full house": None,
            "small straight": None,
            "large straight": None,
            "yahtzee": None,
            "chance": None,
            "upper bonus": 0,
            "yahtzee bonus": 0,
        }
        self.scord_board_upper_list = (
            "ones",
            "twos",
            "threes",
            "fours",
            "fives",
            "sixes",
        )

    def score_bonus(self):
        """Computes and updates the dict with the bonus if any and returns 35 or 0 points to the upper bonus dict value"""
        if (
            sum(
                score
                for category, score in self.board.score_board_dict.items()
                if category in self.board.scord_board_upper_list
            )
            >= 63
        ):
            self.board.score_board_dict["upper bonus"] = 35
        else:
            self.board.score_board_dict["upper bonus"] = 0

    def scores_on_board(self):
        for index, k in enumerate(self.score_board_dict.keys(), start=1):
            if k not in ["yahtzee bonus", "upper bonus"]:
                category_button = tk.Button(
                    self.game.canvas,
                    text=f"{k.title()}",
                    font=(None, 12, "bold"),
                    bg=self.game.main_bg_color,
                    highlightcolor="pink",
                    fg="white",
                    height=0,
                    border=0,
                    state="disabled",
                    disabledforeground="white",
                )
                self.game.category_buttons.append(category_button)
                category_button.place(
                    x=self.game.width // 2, y=40 * index, anchor="s",
                )

    def draw_player_scores(self, slot):
        for index, (category, score) in enumerate(
            self.board.score_board_dict.items(), start=1
        ):
            if category not in ["yahtzee bonus", "upper bonus"]:
                if score is None:
                    score = "-"
                    category_button = tk.Label(
                        self.game.canvas,
                        text=f"{score}",
                        font=(None, 15),
                        bg=self.game.main_bg_color,
                        fg="black",
                    )
                else:
                    category_button = tk.Label(
                        self.game.canvas,
                        text=f"{score}",
                        font=(None, 15),
                        bg=self.game.main_bg_color,
                        fg="black",
                    )
                category_button.place(x=slot, y=40 * index - 2.5, anchor="s")
                self.game.player_scores[
                    category_button["text"].lower()
                ] = category_button

    def end_of_game_score(self):
        """Computes the end of game score including bonus for each player instance call"""
        self.score_bonus()
        self.score_final = sum(
            score for category, score in self.board.score_board_dict.items()
        )
        return self.score_final
