import sys
sys.path.append('.')

from .piece import Piece
from ..position import Position
from ..team import Team

class Knight(Piece):
    def __init__(self, pos: Position, team=Team):
        super().__init__(pos, team)
        
    def move(self, movePos: Position, board):
        dx, dy = [-2, -1, 1, 2, 2, 1, -1, -2], [1, 2, 2, 1, -1, -2, -2, -1]

        for i in range(8):
            x, y = self.pos['x']+dx[i], self.pos['y']+dy[i]
            if (0 <= x < 8) and (0 <= y < 8) and x == movePos['x'] and y == movePos['y'] and self != board[y][x]:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self