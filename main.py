from time import sleep
from os import system

from chess.pieces.pawn import Pawn
from chess.pieces.bishop import Bishop
from chess.pieces.knight import Knight
from chess.pieces.rook import Rook
from chess.pieces.queen import Queen
from chess.pieces.king import King

from chess.position import Position
from chess.team import Team

def clear():
    system('clear')

if __name__ == "__main__":
    chessBoard = [
        [
            Rook(Position(0, 0), Team.BLACK), Knight(Position(1, 0), Team.BLACK), Bishop(Position(2, 0), Team.BLACK), Queen(Position(3, 0), Team.BLACK), King(Position(4, 0), Team.BLACK), Bishop(Position(5, 0), Team.BLACK), Knight(Position(6, 0), Team.BLACK), Rook(Position(7, 0), Team.BLACK)
        ],
        [
            Pawn(Position(x, 1), Team.BLACK) for x in range(8)
        ],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [None for _ in range(8)],
        [
            Pawn(Position(x, 6), Team.WHITE) for x in range(8)
        ],
        [
            Rook(Position(0, 7), Team.WHITE), Knight(Position(1, 7), Team.WHITE), Bishop(Position(2, 7), Team.WHITE), Queen(Position(3, 7), Team.WHITE), King(Position(4, 7), Team.WHITE), Bishop(Position(5, 7), Team.WHITE), Knight(Position(6, 7), Team.WHITE), Rook(Position(7, 7), Team.WHITE)
        ],
    ]
    
    while True:
        clear()
        print("    0    1    2    3    4    5    6    7")
        for idx, line in enumerate(chessBoard):
            print(idx, end=" ")
            for piece in line:
                print(piece, end=" ")
            print(idx)
        print("    0    1    2    3    4    5    6    7")

        curY, curX = list(map(int, input().split()))
        if curX == -1 and curY == -1:
            break
        
        pick = chessBoard[curY][curX]
        if pick == None:
            continue
        print(f"pick: {pick}")
        
        moveY, moveX = list(map(int, input().split()))
        print(f"move: {chessBoard[moveY][moveX]}")

        
        pick.move(Position(moveX, moveY), chessBoard)
        sleep(2)

    print("Exit")