from .piece import Piece
from ..position import Position
from ..team import Team

class Pawn(Piece):
    def __init__(self, pos: Position, team=Team):
        super().__init__(pos, team)
        self.isFirstMove = True

    def move(self, movePos: Position, board) -> bool:
        gap = self.pos - movePos

        if (self.team == Team.BLACK and self.pos['y'] >= movePos['y']) or (self.team == Team.WHITE and self.pos['y'] <= movePos['y']):
            return False

        if gap['x'] == 0:
            if gap['y'] == 1 and board[movePos['y']][movePos['x']] == None:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                return True
            elif gap['y'] == 2 and self.isFirstMove and board[movePos['y']][movePos['x']] == None:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                return True
        elif gap['x'] == 1 and gap['y'] == 1 and self != board[movePos['y']][movePos['x']]:
            board[self.pos['y']][self.pos['x']] = None
            self.pos = movePos
            board[self.pos['y']][self.pos['x']] = self
            return True
        return False