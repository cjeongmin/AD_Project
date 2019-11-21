from .piece import Piece
from ..position import Position
from ..team import Team

class Pawn(Piece):
    def __init__(self, pos: Position, team: Team):
        super().__init__(pos, team)
        self.isFirstMove = True

    def move(self, movePos: Position, board) -> (bool, bool): # (success, promotion)
        gap = self.pos - movePos

        if (self.team == Team.BLACK and self.pos['y'] >= movePos['y']) or (self.team == Team.WHITE and self.pos['y'] <= movePos['y']):
            return (False, False)

        if gap['x'] == 0:
            if gap['y'] == 1 and board[movePos['y']][movePos['x']] == None:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                self.isFirstMove = False
                if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                    return (True, True)
                return (True, False)
            elif gap['y'] == 2 and self.isFirstMove and board[movePos['y']][movePos['x']] == None:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                self.isFirstMove = False
                if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                    return (True, True)
                return (True, False)
        elif gap['x'] == 1 and gap['y'] == 1 and board[movePos['y']][movePos['x']] != None and self != board[movePos['y']][movePos['x']]:   
            board[self.pos['y']][self.pos['x']] = None
            self.pos = movePos
            board[self.pos['y']][self.pos['x']] = self
            self.isFirstMove = False
            if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                return (True, True)
            return (True, False)
        return (False, False)