import sys

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
from chess.check import fillCheckBoard

from gui.board import Board
from PyQt5.QtWidgets import QApplication

from ai.ai import AI

def clear():
    system('clear')

def textTest(chessBoard):
    turn = False
    while True:
        clear()
        whiteCheckBoard, whiteCheck = fillCheckBoard(chessBoard, Team.WHITE) #화이트 킹이 체크인지 아닌지, 왕이 움직일 수 있는 공간 검사
        blackCheckBoard, blackCheck = fillCheckBoard(chessBoard, Team.BLACK) #블랙 킹이 체크인지 아닌지, 옹이 움직일 수 있는 공간 검사
        for line in whiteCheckBoard:
            for e in line:
                print(1 if not(e) else 0, end=" ")
            print()
        print("*"*20)
        print("    0    1    2    3    4    5    6    7")
        for idx, line in enumerate(chessBoard):
            print(idx, end=" ")
            for piece in line:
                print(piece, end=" ")
            print(idx)
        print("    0    1    2    3    4    5    6    7")
        print(("White" if not(turn) else "Black") + "'s turn")
        print(f"Check: {blackCheck if turn else whiteCheck}")

        curY, curX = list(map(int, input().split()))
        if curX == -1 and curY == -1:
            break

        pick = chessBoard[curY][curX]
        if pick == None or pick.team != (Team.WHITE if not(turn) else Team.BLACK):
            continue
        print(f"pick: {pick}")

        moveY, moveX = list(map(int, input().split()))

        if pick.getType() != "King":
            if not(pick.move(Position(moveX, moveY), chessBoard)):
                continue
        else:
            if not(pick.move(Position(moveX, moveY), chessBoard, whiteCheckBoard if not(turn) else blackCheckBoard)):
                # 킹이 움직일 때 실패한 경우 사용자에게 경고를 하는 코드가 필요함.
                continue
        turn = not(turn)

    print("Exit")

def guiTest(chessBoard):
    print(sys.path)
    mode = int(input('Select Mode\n1.Single, 2.AI\n>> '))
    app = QApplication(sys.argv)
    board = Board(chessBoard, AI() if mode == 2 else None)
    sys.exit(app.exec_())

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
    guiTest(chessBoard)
    textTest(chessBoard)