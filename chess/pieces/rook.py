from .piece import Piece
from ..position import Position
from ..team import Team

class Break(Exception):
    pass

class Rook(Piece):
    def __init__(self, pos: Position, team: Team):
        super().__init__(pos, team)
        self.isFirstMove = True

    def move(self, movePos: Position, board):
        # if self.isPin(movePos, board):
        #     return False

        dx, dy = [-1, 0, 1, 0], [0, -1, 0, 1]
        try:
            for i in range(4):
                x, y = self.pos['x'] + dx[i], self.pos['y'] + dy[i]
                while (0 <= x < 8) and (0 <= y < 8) and board[y][x] == None:
                    if x == movePos['x'] and y == movePos['y']:
                        raise Break()
                    x, y = x + dx[i], y + dy[i]
                if (0 <= x < 8) and (0 <= y < 8) and self != board[y][x] and x == movePos['x'] and y == movePos['y']:
                    raise Break()
        except Break:
            if self != board[movePos['y']][movePos['x']]:
                board[self.pos['y']][self.pos['x']] = None
                self.pos = movePos
                board[self.pos['y']][self.pos['x']] = self
                self.isFirstMove = False
                return True
        return False