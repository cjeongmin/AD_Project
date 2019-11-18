import sys
sys.path.append('.')

from .piece import Piece
from ..position import Position

class King(Piece):
    def __init__(self, pos: Position, team=str):
        super().__init__(pos, team)
        self.isChecked = False
        