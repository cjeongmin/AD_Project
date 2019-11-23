from .piece import Piece
from ..position import Position
from ..team import Team

class Pawn(Piece):
    def __init__(self, pos: Position, team: Team):
        super().__init__(pos, team)
        self.isFirstMove = True
        self.dieByEnpassant = False 

    def move(self, movePos: Position, board) -> (bool, bool): # (success, promotion)
        if self.isPin(board):
            return (False, False)

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
                self.dieByEnpassant = 2
                if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                    return (True, True)
                return (True, False)
        elif gap['x'] == 1 and gap['y'] == 1 and self != board[movePos['y']][movePos['x']]:
            # Enpassant
            if self.pos['y'] == (3 if self.team == Team.WHITE else 4) and board[movePos['y']+(1 if self.team == Team.WHITE else -1)][movePos['x']] != None and board[movePos['y']+(1 if self.team == Team.WHITE else -1)][movePos['x']].getType() == "Pawn" and board[movePos['y']+(1 if self.team == Team.WHITE else -1)][movePos['x']].dieByEnpassant == 1:
                board[movePos['y']+(1 if self.team == Team.WHITE else -1)][movePos['x']] = None
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                self.isFirstMove = False
                if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                    return (True, True)
                return (True, False)
            elif board[movePos['y']][movePos['x']] != None:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                self.isFirstMove = False
                if self.pos['y'] == (0 if self.team == Team.WHITE else 7):
                    return (True, True)
                return (True, False)
        return (False, False)