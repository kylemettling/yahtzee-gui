import random
import os
import tkinter as tk
from calculate_score import Scorer

# from player import Player

from scoreboard import ScoreKeeper

from gamegui import GameGui, game


class TurnTaker:
    """Class for a functioning turn per instance of player. Expects nothing but takes calls from the player instance 
    but modifies the dictionary and calls functions from ScoreKeeper"""

    def __init__(self, board):
        """Gives the turn class the number of rolls, dice and turns to start with. 
        Also gives empty lists for roll results and dice chosen to keep and kept dice counter.
        Also points to the board and score instances.
        """
        self.num_dice = 5
        self.num_rolls = 3
        self.roll_result = []
        self.chosen_dice = []
        self.kept_dice = set()
        self.kept_count = 0
        self.turn_count = 0
        self.board = board
        self.game = game
        self.roll_button = self.game.roll_button
        self.var = tk.IntVar()
        self.game.roll_button["command"] = lambda: self.roll()

    def roll(self):
        """Initializes a roll for player instances. Prints a list of randomly selected dice and calls the kept dice function after roll.
        Also decrements number of rolls and passes to Score after roll is complete.
        """
        if self.num_rolls > 0:
            self.roll_button["command"] = lambda: self.var.set(1)
            for _ in range(self.num_dice - self.kept_count):
                self.roll_result.append(random.randint(1, 6))
            self.num_rolls -= 1
            for i in self.roll_result:
                self.init_dice(i)
            self.game.place_dice()
            self.end_of_roll()

    def end_of_roll(self):
        """If num_rolls > 0, sets a wait_variable in order to allow for user dice selection.
        Once user choses to roll again, this function iterates over the kept_dice and appends the roll result item to the chosen dice list,
        clears drawn_dice list, creates list for current roll result, clears chosen dice, sets kept_count to length of kept_dice,
        clears kept_dice and calls roll once more.
        If num_rolls == 0, the buttons are silenced and the program wait for user input to select a category to score for."""
        if self.num_rolls > 0:
            self.roll_button.wait_variable(self.var)
            for index in self.kept_dice:
                self.chosen_dice.append(self.roll_result[index])
            self.game.drawn_dice.clear()
            self.roll_result = [i for i in self.chosen_dice]
            self.chosen_dice.clear()
            self.kept_count = len(self.kept_dice)
            self.kept_dice.clear()
            self.roll()
        else:
            self.roll_button["command"] = ""
            for dice in self.game.drawn_dice:
                dice["command"] = ""
            for category_button in self.game.category_buttons:
                category_button["state"] = "normal"
                if self.board.score_board_dict[category_button["text"].lower()] is None:
                    category_button[
                        "command"
                    ] = lambda category=category_button, roll=self.roll_result, board=self.board: self.score_and_remove_category(
                        category, roll, board
                    )
                else:
                    category_button["command"] = ""
            if self.turn_count < 3:
                self.game.turn_indicator[
                    "text"
                ] = "Click on a category name to score your roll!"
            else:
                self.game.turn_indicator["text"] = "Time to score your roll!"
            self.game.update_idletasks()
            self.game.wait_variable(self.var)

    def init_dice(self, die_num):
        """Expects a die_num and creates a button with the image from the corresponding to the die_num in game.dice_img list.
        Appends the dice button object to the drawn_dice list."""
        dice = tk.Button(
            self.game.canvas,
            image=self.game.dice_imgs[die_num - 1],
            command=lambda: self.keepers(self.game.drawn_dice.index(dice)),
        )
        self.game.drawn_dice.append(dice)

    def get_highlight_dice(self, index):
        """Expects an index. Uses index to assign highlighted image to the drawn dice index's image property."""
        self.game.drawn_dice[index]["image"] = self.game.highlight_imgs[
            self.roll_result[index] - 1
        ]

    def get_nonhighlight_dice(self, index):
        """Expects an index. Uses index to assign non-highlighted image to the drawn dice index's image property."""
        self.game.drawn_dice[index]["image"] = self.game.dice_imgs[
            self.roll_result[index] - 1
        ]

    def keepers(self, index):
        """Expects an index. Keeps track of actively held dice.
        ie: if users highlight then de-highlight a die, the kept_dice is accurate to only highlighted die."""
        if index in self.kept_dice:
            self.kept_dice.remove(index)
            self.get_nonhighlight_dice(index)
        else:
            self.kept_dice.add(index)
            self.get_highlight_dice(index)

    def score_and_remove_category(self, category, roll, board):
        """Expects a category, roll and board parameter. Sets the wait variable to resume program.
        Calls Scorer's score_roll method. Passes the player's current roll and the player's board to Scorer and the chosen category to score_roll.
        Calls end_of_turn()"""
        self.var.set(1)
        Scorer(roll, board).score_roll(category["text"].lower())
        self.end_of_turn()

    def end_of_turn(self):
        """Sets the dice and category button commands to an empty string.
        Increments the turn counter. Then resets chosen dice, kept count, roll count, roll result and calls roll for next turn
        For multiplayer this then leads to the turn change to the next player"""
        for dice in self.game.drawn_dice:
            dice["command"] = ""
        for buttons in self.game.category_buttons:
            buttons["command"] = ""
        self.turn_count += 1
        self.chosen_dice = []
        self.kept_count = 0
        self.num_rolls = 3
        self.roll_result = []
        self.kept_dice.clear()
        self.game.drawn_dice.clear()
