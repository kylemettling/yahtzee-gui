import tkinter as tk
from tkinter import messagebox
import sys
import os


class GameGui(tk.Frame):
    """Class for creating Tkinter instance and setup for use by Yahtzee class. """

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.height = 1020
        self.width = 600
        self.main_bg_color = "#59728f"
        self.popup_frame_bg_color = "#8093A9"
        self.button_bg_color = "#B5C1CF"
        self.canvas = tk.Canvas(
            self.master, height=self.height, width=self.width, bg=self.main_bg_color
        )
        self.title = master.title("Yahtzee")
        self.icon = master.iconbitmap("images/logo_small.ico")
        self.die_height, self.die_width = (200, 200)
        self.dice_imgs = [tk.PhotoImage(file=f"images/die{i}.png") for i in range(1, 7)]
        self.highlight_imgs = [
            tk.PhotoImage(file=f"images/die{i}_highlight.png") for i in range(1, 7)
        ]
        self.drawn_dice = []
        self.category_buttons = []
        self.player_scores = {}
        self.roll_button = tk.Button(
            self.canvas,
            text="ROLL",
            font=(None, 16, "bold"),
            bg=self.button_bg_color,
            activebackground=self.button_bg_color,
        )
        self.turn_indicator = tk.Label(
            self.canvas, bg=self.main_bg_color, fg="black", font=(None, 16, "bold")
        )
        self.end_frame = tk.Frame(
            self.master,
            bg=f"{self.popup_frame_bg_color}",
            relief="ridge",
            borderwidth=10,
        )
        self.end_frame_x, self.end_frame_y = (
            self.width // 2,
            self.width // 1.5,
        )
        self.main_widget()

    def main_widget(self):
        """Packs canvas to the screen"""
        # self.canvas
        self.canvas.pack()

    def close_game(self):
        """Calls destory on root object and calls for system exit."""
        # root.quit()
        # root.withdraw()
        root.destroy()
        sys.exit()
        # game.destroy()
        # root.destroy()

    def draw_roll_button(self):
        """Places the roll button on screen."""
        self.roll_button.place(
            x=(self.width // 2),
            y=(self.height - (self.die_height * 2) - 10),
            anchor="s",
            height=40,
            width=150,
        )

    def display_start_screen_text(self, message):
        """Expects a message to be used. Creates and places a label object on the screen with the given message as text."""
        self.start_screen_text = tk.Label(
            self.canvas, text=f"{message}", font=(None, 25), bg=self.main_bg_color
        )
        self.start_screen_text.place(
            x=self.width / 2,
            y=self.height / 3 + 40,
            anchor="center",
            height=150,
            width=500,
        )

    def draw_turn_indicator(self):
        """Places the turn indicator on the screen."""
        self.turn_indicator.place(
            x=self.width // 2, y=(self.roll_button.winfo_y() - 20), anchor="center"
        )

    def place_dice(self):
        """Iterates over the drawn_dice list and placement list to place dice in 
        intended positions of three dice in row at bottom of screen and two dice centered above the bottom row"""
        for index, (dice, placement) in enumerate(
            zip(self.drawn_dice, [0, 0, 1, 0, 2]), start=1
        ):
            if index == 2:
                dice.place(
                    x=(self.width / 2),
                    y=(self.height - (self.die_height * 2) - 8),
                    anchor="ne",
                )
            elif index == 4:
                dice.place(
                    x=(self.width / 2),
                    y=(self.height - self.die_height * 2 - 8),
                    anchor="nw",
                )
            else:
                dice.place(
                    x=(self.die_width * placement),
                    y=(self.height - self.die_height - 2),
                    anchor="nw",
                )


root = tk.Tk()

game = GameGui(root)


def on_close():
    """Creates messagebox object to prompt "yes or no?" to user when main window Close/Exit ("X") button is clicked.
    If user choses yes, root Tkinter instance is destroyed and os._exit(1) terminates program."""
    close = messagebox.askokcancel("Yahtzee", "Would you like to close the program?")
    if close:
        root.destroy()
        os._exit(1)


root.protocol("WM_DELETE_WINDOW", on_close)
