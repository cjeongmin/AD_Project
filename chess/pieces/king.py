from .piece import Piece
from ..position import Position
from ..team import Team

class King(Piece):
    def __init__(self, pos: Position, team: Team):
        super().__init__(pos, team)
        self.isFirstMove = True
        self.isCheck = False

    def move(self, movePos: Position, board, checkboard):
        dx, dy = [0, 1, 1, 1, 0, -1, -1, -1], [1, 1, 0, -1, -1, -1, 0, 1]
        gap = self.pos - movePos

        if gap['y'] == 0 and gap['x'] == 2:
            # Queen side
            if self.isFirstMove and not(self.isCheck) and board[movePos['y']][1] == None and board[movePos['y']][2] == None and board[movePos['y']][3] == None and board[movePos['y']][0].getType() == "Rook" and board[movePos['y']][0].isFirstMove and checkboard[movePos['y']][2] and checkboard[movePos['y']][3]:
                # King move
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                # Rook move
                board[self.pos['y']][0].pos = Position(3, self.pos['y'])
                board[self.pos['y']][3] = board[self.pos['y']][0]
                board[self.pos['y']][0] = None
                self.isFirstMove = False
                board[self.pos['y']][3].isFirstMove = False
                return True
            # King side
            elif self.isFirstMove and not(self.isCheck) and board[movePos['y']][5] == None and board[movePos['y']][6] == None and board[movePos['y']][7].getType () == "Rook" and board[movePos['y']][7].isFirstMove and checkboard[movePos['y']][5] and checkboard[movePos['y']][6]:
                # King move
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                # Rook move
                board[self.pos['y']][7].pos = Position(5, self.pos['y'])
                board[self.pos['y']][5] = board[self.pos['y']][7]
                board[self.pos['y']][7] = None
                self.isFirstMove = False
                board[self.pos['y']][5].isFirstMove = False
                return True
        else:
            for i in range(8):
                x, y = self.pos['x']+dx[i], self.pos['y']+dy[i]
                if (0 <= x < 8) and (0 <= y < 8) and x == movePos['x'] and y == movePos['y'] and self != board[y][x] and checkboard[y][x]:
                    board[self.pos['y']][self.pos['x']] = None
                    self.pos = movePos
                    board[self.pos['y']][self.pos['x']] = self
                    self.isFirstMove = False
                    return True
        return False