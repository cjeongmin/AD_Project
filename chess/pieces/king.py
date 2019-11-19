from .piece import Piece
from ..position import Position
from ..team import Team

class King(Piece):
    def __init__(self, pos: Position, team=Team):
        super().__init__(pos, team)
        self.isChecked = False

    def move(self, movePos: Position, board, checkboard):
        dx, dy = [0, 1, 1, 1, 0, -1, -1, -1], [1, 1, 0, -1, -1, -1, 0, 1]

        for i in range(8):
            x, y = self.pos['x']+dx[i], self.pos['y']+dy[i]
            if (0 <= x < 8) and (0 <= y < 8) and x == movePos['x'] and y == movePos['y'] and self != board[y][x] and checkboard[y][x]:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                return True
        return False