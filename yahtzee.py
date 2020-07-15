from gamegui import GameGui, game, root, on_close
from player import Player
from scoreboard import ScoreKeeper
from tkinter import messagebox
import sys
import tkinter as tk
import json
import os


class Yahtzee(GameGui, Player):
    """Yahtzee class to handle macro game setup and mechanics. Inherits from GameGui and Player."""

    def __init__(self):
        self.game = game
        self.canvas = self.game.canvas
        self.active_players = []
        self.highscore_labels = []
        self.player_count = len(self.active_players)
        self.scores_file = "highscores.json"
        self.placed_highscore_items = []
        self.var = tk.IntVar()
        self.board = ScoreKeeper()
        self.ask_for_players()

    def ask_for_players(self):
        """Displays and positions the initial title text and player count select buttons.
        The buttons expect user input for desired player count.
        Once selected, it calls the setup_game function and passes the player count to it. """
        self.game.display_start_screen_text(
            "Welcome to Yahtzee\nHow many players are there?"
        )
        one_player_button = tk.Button(
            self.game.canvas,
            text="One Player",
            command=lambda: self.setup_game(1, buttons),
            bg=self.game.button_bg_color,
        )
        one_player_button.place(
            x=self.game.width // 2, y=self.game.height // 3 + 150, anchor="e"
        )
        two_player_button = tk.Button(
            self.game.canvas,
            text="Two Player",
            command=lambda: self.setup_game(2, buttons),
            bg=self.game.button_bg_color,
        )
        two_player_button.place(
            x=self.game.width // 2, y=self.game.height // 3 + 150, anchor="w"
        )
        buttons = one_player_button, two_player_button
        self.game.roll_button["state"] = "disabled"

    def setup_game(self, player_count, buttons):
        """Expects a player count and button objects. 
        Initializes a Player class instance for the desired player amount. 
        Destroys the start screen text and buttons and calls the main_game_start function"""
        for amount in range(1, player_count + 1):
            self.active_players.append(Player(f"player{amount}"))
        for item in buttons:
            item.destroy()
        self.game.start_screen_text.destroy()
        self.main_game_start()

    def main_game_start(self):
        """Activates the roll_button. Calls the place_player_name_frame function.
        Draws the categories to the screen. Creates a dictionary for storing column position in key of player name.
        Iterates through active_players and calls draw_player_score to display player names in column positions.
        Starts a while loop for the main Yahtzee turn taking logic and ends when the last player reaches the last turn.
        Main Yahtzee logic includes calling each player's roll function and then calls the update scores to refresh current score amounts.
        Calls the end_of_game_display and end_of_game_text functions and then the get_final_scores and store_player_scores functions
        which presents the end of game screen for the player's to decide next action Play Again, View Highscores or Quit Game."""
        self.game.roll_button["state"] = "active"
        self.place_player_name_frame()
        self.game.draw_roll_button()
        self.board.scores_on_board()
        self.player_score_column = {
            k: v
            for k, v in zip(
                self.active_players, [self.game.width // 4, self.game.width // 4 * 3]
            )
        }
        for player in self.active_players:
            player.draw_player_scores(self.player_score_column[player])
            self.draw_player_name(player)
        while self.active_players[-1].turn_count < 13:
            for i in self.active_players:
                self.game.turn_indicator["text"] = f"{i.name.title()}'s turn"
                self.game.after(1, self.game.draw_turn_indicator)
                self.game.update_idletasks()
                i.roll()
                self.update_scores()
        self.end_of_game_display()
        self.end_of_game_text()
        # self.get_final_scores()
        self.store_player_scores()

    def place_player_name_frame(self):
        """Displays frame for holding name selection input and enter button. Calls place_player_name_form function."""
        self.prompt_frame = tk.Frame(
            self.canvas, bg=self.game.popup_frame_bg_color, bd=5, relief="ridge"
        )
        self.prompt_frame_x, self.prompt_frame_y = (
            self.game.height // 20,
            self.game.height // 4.5,
        )
        self.prompt_frame.place(
            height=self.prompt_frame_x + 30,
            width=self.prompt_frame_y,
            x=self.game.width // 2,
            y=(self.game.height - (self.game.die_height * 2) - 10),
            anchor="center",
        )
        self.place_player_name_form()

    def place_player_name_form(self):
        """Creates and displays entry form and button asking user to input custom names for each player in active_players.
        Binds left mouse button to the entry form to clear preset text and also the retrun key to submit name.
        Assigns name_player_count a starting value of 0 to correspond submitted names with the player instances in active_players.
        Sets a wait variable after each name entry to pause until the total amount of players have names assigned and then destroys the prompt_frame."""
        self.name_form = tk.Entry(
            self.prompt_frame,
            bg=self.game.popup_frame_bg_color,
            fg="black",
            font=(None, 12),
        )
        self.name_form.bind("<Button-1>", self.clear_form)
        self.name_form.bind("<Return>", lambda x: self.submit_name(_))
        self.name_form.place(
            height=self.prompt_frame_x // 2,
            width=self.prompt_frame_y * 5 / 7,
            x=8,
            y=8,
            anchor="nw",
        )
        self.game.update_idletasks()
        self.named_player_count = 0
        for index, _ in enumerate(range(len(self.active_players)), start=1):
            self.name_form.insert(12, f"Enter player {index}'s name")
            self.name_button = tk.Button(
                self.prompt_frame,
                bg=self.game.button_bg_color,
                activebackground=self.game.button_bg_color,
                text="Enter",
                command=lambda: self.submit_name(_),
            )
            self.name_button.place(
                height=self.prompt_frame_x // 2,
                width=self.prompt_frame_y * 1 / 5,
                x=self.name_form.winfo_width(),
                y=8,
            )
            self.game.wait_variable(self.var)
        self.prompt_frame.destroy()

    def clear_form(self, event):
        """Clears entry form."""
        self.name_form.delete(0, "end")

    def submit_name(self, event):
        """Expects an event from either name selection entry form or button.
        Calls set_player_name passing the current Player instance.
        Calls clear_form to delete current text in entry form.
        Sets the wait variable to 1 which allows the next player to select name or returns to next call in main_game_start."""
        self.set_player_name(self.active_players[self.named_player_count])
        self.clear_form(0)
        self.named_player_count += 1
        self.var.set(1)

    def set_player_name(self, player):
        """Expects the player instance position in active_players list. Gets and assigns entry form text to player.name."""
        player.name = f"{self.name_form.get()}"

    def draw_player_name(self, player):
        """Creates and alignment index to draw player names in position under each player's score column."""
        name_alignment_index = {1: 1, 2: 3}
        name_label = tk.Label(
            self.canvas,
            bg=f"{self.game.main_bg_color}",
            fg="black",
            text=f"{player.name.title()}",
            font=(None, 12, "underline"),
        )
        self.game.update_idletasks()
        x, y = (
            (self.game.width // 4) * name_alignment_index[player.id],
            (self.game.category_buttons[-1].winfo_y() + 40),
        )
        name_label.place(x=x, y=y, anchor="center")

    def update_scores(self):
        """Calls the Tkinter after function to then call a lambda to call draw_player_scores for each player.
        This is needed to draw current score to the screen."""
        self.game.after(
            1,
            lambda: [
                player.draw_player_scores(self.player_score_column[player])
                for player in self.active_players
            ],
        )

    def store_player_scores(self):
        """Try and except block to look for a JSON scores_file. Either assigns loaded json to json_data or sets up initial object to be dumped and added to.
        Iterates over active_players and appends the player name and end_of_game_score function to the JSON list object and dumps the updated object."""
        try:
            with open(self.scores_file) as f:
                json_data = json.load(f)
        except FileNotFoundError:
            json_data = {"player_scores": []}
        for player in self.active_players:
            new_score_list = {"name": player.name, "score": player.end_of_game_score()}
            json_data["player_scores"].append(new_score_list)

        with open(self.scores_file, "w") as f:
            json.dump(json_data, f)

    def get_highscores(self):
        """Opens newly updated JSON file and assigns the load to json_data. 
        Sorts the list of player scores dictionaries by score and creates Tkinter label objects for the Top 10 scores."""
        with open(self.scores_file) as f:
            json_data = json.load(f)
        sorted_scores = sorted(
            json_data["player_scores"], key=lambda i: i["score"], reverse=True
        )
        for index, (score, name) in enumerate(
            ((i["score"], i["name"]) for i in sorted_scores[:10]), start=1
        ):
            highscore_item = tk.Label(
                self.game.end_frame,
                text=f"{index}.  {name}  {score}",
                font=(None, 12, "bold"),
                bg=f"{self.game.popup_frame_bg_color}",
                height=1,
            )
            self.highscore_labels.append(highscore_item)

    def display_highscores(self):
        """Clears the highscore_labels list. Calls get_highscores and end_of_game_display functions.
        Creates a Highscores title label and iterates over the newly updated highscores list and places the list items on the screen."""
        self.highscore_labels.clear()
        self.get_highscores()
        self.end_of_game_display()
        self.game.update_idletasks()
        title = tk.Label(
            self.game.end_frame,
            text="Highscores",
            font=(None, 14, "bold underline"),
            bg=f"{self.game.popup_frame_bg_color}",
        )
        title_place = title.place(
            x=self.game.end_frame_x // 2 - self.game.end_frame["borderwidth"],
            y=self.game.end_frame_y // 11,
            anchor="s",
        )
        self.placed_highscore_items.append(title_place)
        self.game.update_idletasks()
        for index, highscore in enumerate(self.highscore_labels, start=2):
            self.game.update_idletasks()
            placed_highscore = highscore.place(
                x=self.game.end_frame_x // 3 - self.game.end_frame["borderwidth"],
                y=self.game.end_frame_y // 11 * index // 1.25,
                anchor="w",
            )
            self.placed_highscore_items.append(placed_highscore)

    def get_final_scores(self):
        """Creates a list containing player.end_of_game_score function calls.
        Creates a dictionary for holding player scores with active_player instances as keys. Sorts the dictionary by highest score."""
        scores = [player.end_of_game_score() for player in self.active_players]
        self.player_score_dict = {k: v for (k, v) in zip(self.active_players, scores)}
        self.sort_scores = sorted(
            self.player_score_dict.items(), key=lambda x: x[1], reverse=True
        )

    def end_of_game_display(self):
        """Places end_of_game_display to the screen and calls the end_of_game_button function."""
        self.game.end_frame.place(
            height=self.game.end_frame_y,
            width=self.game.end_frame_x,
            x=self.game.width // 2,
            y=self.game.height // 3 * 2,
            anchor="center",
        )
        self.game.update_idletasks()
        self.end_of_game_buttons()

    def end_of_game_text(self):
        """Assigns the leading score from a sorted list to a winner variable. 
        If block for deciding and creating different end_frame labels for one and two player modes.
        Calls display_bonus_scores function.
        """
        winner = "".join(
            sorted(
                self.active_players, key=lambda x: x.end_of_game_score(), reverse=True,
            )[0].name
        )
        if len(self.active_players) > 1:
            congrats = f"Congratulations {winner.title()}!"
            display_winner = tk.Label(
                self.game.end_frame,
                text=f"{congrats}",
                font=(None, 18, "bold"),
                bg=self.game.popup_frame_bg_color,
            )
        else:
            game_over = f"Game over!"
            display_winner = tk.Label(
                self.game.end_frame,
                text=f"{game_over}",
                font=(None, 18, "bold"),
                bg=self.game.popup_frame_bg_color,
            )
        self.game.update_idletasks()
        display_player_final_scores = [
            tk.Label(
                self.game.end_frame,
                text=f"{player.name.title()}\n {player.end_of_game_score()}",
                font=(None, 14, "bold"),
                bg=self.game.popup_frame_bg_color,
            )
            for player in self.active_players
        ]
        if len(self.active_players) != 1:
            place_players = [
                (
                    label.place(
                        x=(self.game.end_frame_x // 4 * index) - 15,
                        y=self.game.end_frame_y // 2,
                        anchor="center",
                    )
                )
                for label, index in zip(display_player_final_scores, range(1, 4, 2))
            ]
        else:

            place_players = [
                (
                    label.place(
                        x=(self.game.end_frame_x // 2) - 10,
                        y=self.game.end_frame_y // 2,
                        anchor="center",
                    )
                )
                for label in display_player_final_scores
            ]
            display_player_final_scores[0][
                "text"
            ] = f"Your final score was\n{self.active_players[0].end_of_game_score()}"
        display_winner.place(
            x=self.game.end_frame_x // 2 - self.game.end_frame["borderwidth"],
            y=self.game.end_frame_y // 4,
            anchor="center",
        )
        self.display_bonus_scores()

    def display_bonus_scores(self):
        """Creates an alignment dictionary for each of the bonus categories.
        Iterates through a zipping of active_players and index range. Index range is used as a multiplier for aligning along Y-axis.
        Iterates over each players bonus categories and creates labels for displaying them."""
        bonus_category_alignment_dict = {"upper bonus": 40, "yahtzee bonus": 60}
        for index, player in zip(range(1, 4, 2), self.active_players):
            if len(self.active_players) < 2:
                index = 2
            for _, (category, score), in enumerate(
                player.board.score_board_dict.items()
            ):
                if category in bonus_category_alignment_dict.keys():
                    category_label = tk.Label(
                        self.game.end_frame,
                        text=f"{category.title()}: {score}",
                        font=(None, 12),
                        bg=self.game.popup_frame_bg_color,
                    )
                    category_label.place(
                        x=(self.game.end_frame_x // 4 * index) - 10,
                        y=self.game.end_frame_y // 2
                        + bonus_category_alignment_dict[category],
                        anchor="center",
                    )
                    self.game.update_idletasks()

    def end_of_game_buttons(self):
        """Creates buttons to be drawn to the screen for Play Again, View Highscores and Quit Game functions.
        Assigns button commands as lambda functions to each corresponding option."""
        play_again = tk.Button(
            self.game.end_frame,
            text="Play Again",
            font=(None, 9, "bold"),
            bg=self.game.button_bg_color,
        )
        view_highscores = tk.Button(
            self.game.end_frame,
            text="Highscores",
            font=(None, 9, "bold"),
            bg=self.game.button_bg_color,
        )
        quit_game = tk.Button(
            self.game.end_frame,
            text="Quit Game",
            font=(None, 9, "bold"),
            bg=self.game.button_bg_color,
        )
        buttons_command_dict = {
            play_again: lambda: self.play_again,
            view_highscores: lambda: self.view_highscores,
            quit_game: lambda: self.quit_game,
        }
        self.game.update_idletasks()
        for index, (button, command) in enumerate(
            buttons_command_dict.items(), start=1
        ):
            button.place(
                x=self.game.end_frame_x // 4 * index
                - self.game.end_frame["borderwidth"],
                y=self.game.end_frame_y
                - button.winfo_height()
                - (self.game.end_frame["borderwidth"] * 2),
                anchor="s",
            )
            button["command"] = command()

    def play_again(self):
        """Clears the master frame widget and deletes the instances in active_players and clears the active_players list.
        Calls Yahtzee __init__ method to restart the game from the beginning."""
        master_frame_items = self.get_widget_children(self.game.master)
        for item in master_frame_items:
            item.place_forget()
        for player in self.active_players:
            player.delete_player()
        self.active_players.clear()
        self.game.update_idletasks()
        self.__init__()

    def view_highscores(self):
        """Clears the end_frame widget and calls the display_highscores function."""
        end_frame_items = self.get_widget_children(self.game.end_frame)
        for item in end_frame_items:
            item.place_forget()
        self.display_highscores()

    def quit_game(self):
        """Calls the close_game function to destroy the root Tkinter instance and calls sys.exit()."""
        self.game.close_game()

    def get_widget_children(self, widget):
        """Assigns list of child objects to a widgets variable and iterates over given widget to extend list to all children related to the widget.
        Returns the list of widget child objects"""
        widget_objects = widget.winfo_children()
        for item in widget_objects:
            if item.winfo_children():
                widget_objects.extend(item.winfo_children())
        return widget_objects


start = Yahtzee()
start.game.mainloop()
