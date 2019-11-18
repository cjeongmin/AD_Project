from abc import ABCMeta, abstractmethod

from ..position import Position
from ..team import Team

"""
    참고)
    '_'가 접두사로 하나 붙어 있으면 protected로써 작동하고,
    '_'가 접두사로 두 개 붙어 있으면 private로써 작동함.
"""

class Piece(metaclass=ABCMeta):
    __KINDS = ["Pawn", "Bishop", "Knight", "Rook", "Queen", "King"] # private

    def __init__(self, pos: Position, team: Team):
        self.pos = pos
        self.team = team

    @abstractmethod
    def move(self, movePos: Position, board):
        raise NotImplementedError("The method not implemented.")

    def getType(self) -> str:
        return type(self).__name__

    def __str__(self):
        return f"[{str(self.team)[5]}{type(self).__name__[0]}]"

    def __eq__(self, other) -> bool:
        if type(other).__name__ not in self.__KINDS:
            return False
        
        if self.team == other.team:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not(self == other)