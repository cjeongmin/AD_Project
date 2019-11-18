import sys
sys.path.append('..')

from ..position import Position
from ..team import Team

class Piece:
    KINDS = ["Pawn", "Bishop", "Knight", "Rook", "Queen", "King"]

    def __init__(self, pos: Position, team: Team):
        self.pos = pos
        self.team = team

    def move(self, movePos: Position, board):
        raise NotImplementedError("The method not implemented.")

    def getType(self) -> str:
        return type(self).__name__

    def __str__(self):
        return f"[{str(self.team)[5]}{type(self).__name__[0]}]"

    def __eq__(self, other) -> bool:
        if type(other).__name__ not in self.KINDS:
            return False
        
        if self.team == other.team:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not(self == other)