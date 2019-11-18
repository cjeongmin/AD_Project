from .piece import Piece
from ..position import Position
from ..team import Team

class King(Piece):
    def __init__(self, pos: Position, team=Team):
        super().__init__(pos, team)
        self.isChecked = False

    def move(self):
        return