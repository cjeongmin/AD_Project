from .piece import Piece
from ..position import Position
from ..team import Team

class Break(Exception):
    pass

class Bishop(Piece):
    def __init__(self, pos: Position, team=Team):
        super().__init__(pos, team)

    def move(self, movePos: Position, board):
        dx, dy = [-1, 1, 1, -1], [1, 1, -1, -1]
        try:
            for i in range(4):
                x, y = self.pos['x'] + dx[i], self.pos['y'] + dy[i]
                while (0 <= x < 8) and (0 <= y < 8):
                    if x == movePos['x'] and y == movePos['y'] and self != board[y][x]:
                        raise Break()
                    x, y = x + dx[i], y + dy[i]
                if (0 <= x < 8) and (0 <= y < 8) and self != board[y][x] and x == movePos['x'] and y == movePos['y']:
                    raise Break()
        except Break:
            if self != board[movePos['y']][movePos['x']]:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                return True
        return False