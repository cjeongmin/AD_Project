from abc import ABCMeta, abstractmethod

from ..position import Position
from ..team import Team

"""
    참고)
    '_'가 접두사로 하나 붙어 있으면 protected로써 작동하고,
    '_'가 접두사로 두 개 붙어 있으면 private로써 작동함.
"""

class Break(Exception):
    pass

class Piece(metaclass=ABCMeta):
    __KINDS = ("Pawn", "Bishop", "Knight", "Rook", "Queen", "King") # private

    def __init__(self, pos: Position, team: Team):
        self.pos = pos
        self.team = team

    @abstractmethod
    def move(self, movePos: Position, board) -> bool:
        raise NotImplementedError("The method not implemented.")

    def isPin(self, movePos: Position, board) -> bool: 
        diagonalDx, diagonalDy = [[-1, 1], [1, -1]], [[-1, 1], [-1, 1]]
        straightDx, straightDy = [[-1, 1], [0, 0]], [[0, 0], [1, -1]]
        # 대각선
        for i in range(2):
            x, y = self.pos['x']+diagonalDx[i][0], self.pos['y']+diagonalDy[i][0]
            checkBishopOrQueen, checkKing, canMove = False, False, False
            while (0 <= x < 8 and 0 <= y < 8) and board[y][x] == None:
                if movePos['x'] == x and movePos['y'] == y:
                    canMove = True
                x, y = x+diagonalDx[i][0], y+diagonalDy[i][0]
            if (0 <= x < 8 and 0 <= y < 8):
                if board[y][x] == self and board[y][x].getType() == "King":
                    checkKing = True
                elif board[y][x] != self and board[y][x].getType() == "Bishop" or board[y][x].getType() == "Queen":
                    checkBishopOrQueen = True
                    if movePos['x'] == x and movePos['y'] == y:
                        canMove = True

            x, y = self.pos['x']+diagonalDx[i][1], self.pos['y']+diagonalDy[i][1]
            while (0 <= x < 8 and 0 <= y < 8) and board[y][x] == None:
                if movePos['x'] == x and movePos['y'] == y:
                    canMove = True
                x, y = x+diagonalDx[i][1], y+diagonalDy[i][1]
            if (0 <= x < 8 and 0 <= y < 8):
                if board[y][x] == self and board[y][x].getType() == "King":
                    checkKing = True
                elif board[y][x] != self and board[y][x].getType() == "Bishop" or board[y][x].getType() == "Queen":
                    checkBishopOrQueen = True
                    if movePos['x'] == x and movePos['y'] == y:
                        canMove = True

            if checkBishopOrQueen and checkKing and not canMove:
                return True

        # 직선
        for i in range(2):
            x, y = self.pos['x']+straightDx[i][0], self.pos['y']+straightDy[i][0]
            checkRookOrQueen, checkKing, canMove = False, False, False
            while (0 <= x < 8 and 0 <= y < 8) and board[y][x] == None:
                if movePos['x'] == x and movePos['y'] == y:
                    canMove = True
                x, y = x+straightDx[i][0], y+straightDy[i][0]
            if (0 <= x < 8 and 0 <= y < 8):
                if board[y][x] == self and board[y][x].getType() == "King":
                    checkKing = True
                elif board[y][x] != self and board[y][x].getType() == "Rook" or board[y][x].getType() == "Queen":
                    checkRookOrQueen = True
                    if movePos['x'] == x and movePos['y'] == y:
                        canMove = True

            x, y = self.pos['x']+straightDx[i][1], self.pos['y']+straightDy[i][1]
            while (0 <= x < 8 and 0 <= y < 8) and board[y][x] == None:
                if movePos['x'] == x and movePos['y'] == y:
                    canMove = True
                x, y = x+straightDx[i][1], y+straightDy[i][1]
            if (0 <= x < 8 and 0 <= y < 8):
                if board[y][x] == self and board[y][x].getType() == "King":
                    checkKing = True
                elif board[y][x] != self and board[y][x].getType() == "Rook" or board[y][x].getType() == "Queen":
                    checkRookOrQueen = True
                    if movePos['x'] == x and movePos['y'] == y:
                        canMove = True

            if checkRookOrQueen and checkKing and not canMove:
                return True
        return False

    def getType(self) -> str:
        return type(self).__name__

    def __str__(self):
        return f"[{str(self.team)[5]}{type(self).__name__[0]}]"

    # Equal
    def __eq__(self, other) -> bool:
        if type(other).__name__ not in self.__KINDS:
            return False
        
        if self.team == other.team:
            return True
        return False

    # Not Equal
    def __ne__(self, other) -> bool:
        return not(self == other)