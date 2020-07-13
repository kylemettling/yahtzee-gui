from turn import TurnTaker
from calculate_score import Scorer
from scoreboard import ScoreKeeper


class Player(TurnTaker, ScoreKeeper):
    """Initializes a player instance and inherits from TurnTaker and ScoreKeeper classes to be used for each Player instance."""

    _counter = 0

    def __init__(self, name):
        """Expects a name for the instance.
        Initializes the player class to inherit from the TurnTaker Score and ScoreKeeper classes"""

        ScoreKeeper.__init__(self)
        self.board = ScoreKeeper()
        TurnTaker.__init__(self, self.board)
        Player._counter += 1
        self.name = name
        self.id = Player._counter

    def delete_player(self):
        """Decrements Player class _counter variable by 1 and deletes self."""
        Player._counter -= 1
        del self
